/**
 * Manee Brides API Worker
 * ─────────────────────────────
 * Phase 1: POST /api/upload         → R2 图片上传
 * Phase 2: POST /api/diagnostic-submit → Supabase 表单提交
 * Phase 3: POST /api/stripe-webhook  → Stripe 支付回调
 *          GET  /api/submission-status/:id → 查询支付状态
 * Phase 4: (预留) GET /api/diagnostic/:id 等
 */

// ═══════════════════════════════════════
//  CORS 工具
// ═══════════════════════════════════════

function getAllowedOrigin(request, env) {
  const origin = request.headers.get('Origin') || '';
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim());
  // 开发时允许 localhost
  if (origin.includes('localhost') || origin.includes('127.0.0.1')) return origin;
  if (allowed.includes(origin)) return origin;
  return allowed[0] || '';
}

function corsHeaders(request, env) {
  return {
    'Access-Control-Allow-Origin': getAllowedOrigin(request, env),
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

function jsonResponse(data, status = 200, request, env) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(request, env),
    },
  });
}

function errorResponse(message, status = 400, request, env) {
  return jsonResponse({ error: message }, status, request, env);
}

// ═══════════════════════════════════════
//  路由
// ═══════════════════════════════════════

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // CORS preflight
    if (method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(request, env),
      });
    }

    try {
      // Phase 1: 图片上传
      if (method === 'POST' && path === '/api/upload') {
        return await handleUpload(request, env);
      }

      // Phase 2: 表单提交
      if (method === 'POST' && path === '/api/diagnostic-submit') {
        return await handleDiagnosticSubmit(request, env);
      }

      // Phase 3: Stripe Webhook
      if (method === 'POST' && path === '/api/stripe-webhook') {
        return await handleStripeWebhook(request, env);
      }

      // Phase 3: 查询支付状态
      if (method === 'GET' && path.startsWith('/api/submission-status/')) {
        const id = path.replace('/api/submission-status/', '');
        return await handleSubmissionStatus(id, request, env);
      }

      // R2 文件代理访问
      if (method === 'GET' && path.startsWith('/api/file/')) {
        const fileKey = path.replace('/api/file/', '');
        return await handleFileProxy(fileKey, request, env);
      }

      // Phase 4: 预留端点
      // GET /api/diagnostic/:id
      // GET /api/diagnostics?status=paid
      // POST /api/diagnostic/:id/wechat-status

      // 404
      return errorResponse('Not Found', 404, request, env);

    } catch (err) {
      console.error('Worker error:', err);
      return errorResponse('Internal Server Error: ' + err.message, 500, request, env);
    }
  },
};

// ═══════════════════════════════════════
//  Phase 1: 图片上传
// ═══════════════════════════════════════

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

async function handleUpload(request, env) {
  const contentType = request.headers.get('Content-Type') || '';

  if (!contentType.includes('multipart/form-data')) {
    return errorResponse('请使用 multipart/form-data 上传', 400, request, env);
  }

  const formData = await request.formData();
  const file = formData.get('file');

  if (!file || !(file instanceof File)) {
    return errorResponse('缺少文件', 400, request, env);
  }

  // 校验类型
  if (!ALLOWED_TYPES.includes(file.type)) {
    return errorResponse(`不支持的文件类型: ${file.type}。仅支持 JPG/PNG/WebP/GIF`, 400, request, env);
  }

  // 校验大小
  if (file.size > MAX_FILE_SIZE) {
    return errorResponse('文件过大，最大 10MB', 400, request, env);
  }

  // 生成唯一 key
  const timestamp = Date.now();
  const randomId = crypto.randomUUID().slice(0, 8);
  const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_');
  const fileKey = `uploads/${timestamp}_${randomId}_${safeName}`;

  // 写入 R2
  await env.UPLOADS.put(fileKey, file.stream(), {
    httpMetadata: {
      contentType: file.type,
    },
    customMetadata: {
      originalName: file.name,
      uploadedAt: new Date().toISOString(),
    },
  });

  // 构造访问 URL (通过 Worker 代理)
  const fileUrl = `${new URL(request.url).origin}/api/file/${fileKey}`;

  return jsonResponse({
    success: true,
    fileKey,
    fileUrl,
    fileName: file.name,
    fileSize: file.size,
    fileType: file.type,
  }, 200, request, env);
}

// ═══════════════════════════════════════
//  R2 文件代理 (读取已上传图片)
// ═══════════════════════════════════════

async function handleFileProxy(fileKey, request, env) {
  const object = await env.UPLOADS.get(fileKey);
  if (!object) {
    return errorResponse('文件不存在', 404, request, env);
  }

  const headers = new Headers();
  headers.set('Content-Type', object.httpMetadata?.contentType || 'application/octet-stream');
  headers.set('Cache-Control', 'public, max-age=31536000, immutable');
  // CORS for images
  const origin = getAllowedOrigin(request, env);
  if (origin) headers.set('Access-Control-Allow-Origin', origin);

  return new Response(object.body, { headers });
}

// ═══════════════════════════════════════
//  Phase 2: 诊断表单提交
// ═══════════════════════════════════════

async function handleDiagnosticSubmit(request, env) {
  const body = await request.json();

  // 基本验证
  if (!body.userName || !body.userWechat) {
    return errorResponse('名字和微信号为必填项', 400, request, env);
  }

  // 构造记录
  const record = {
    user_name: body.userName,
    user_wechat: body.userWechat,
    user_job: body.userJob || null,
    user_age: body.userAge || null,
    platform: body.platform || null,
    goals: body.goals || [],
    pain_point: body.painPoint || null,
    styles: body.styles || [],
    personal_photos: body.personalPhotos || [],
    ref_photos: body.refPhotos || [],
    direction: body.direction || null,
    user_note: body.userNote || null,
    payment_status: 'pending',
    payment_amount: 2900, // $29 USD (cents)
    ip_address: request.headers.get('CF-Connecting-IP') || '',
    user_agent: request.headers.get('User-Agent') || '',
  };

  // 插入 Supabase
  const supabaseUrl = env.SUPABASE_URL;
  const supabaseKey = env.SUPABASE_SERVICE_KEY;

  if (!supabaseUrl || !supabaseKey) {
    return errorResponse('后端配置错误：缺少数据库凭证', 500, request, env);
  }

  const res = await fetch(`${supabaseUrl}/rest/v1/diagnostic_submissions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apikey': supabaseKey,
      'Authorization': `Bearer ${supabaseKey}`,
      'Prefer': 'return=representation',
    },
    body: JSON.stringify(record),
  });

  if (!res.ok) {
    const errText = await res.text();
    console.error('Supabase insert error:', errText);
    return errorResponse('数据保存失败，请稍后重试', 500, request, env);
  }

  const [inserted] = await res.json();

  return jsonResponse({
    success: true,
    submissionId: inserted.id,
    message: '提交成功',
  }, 200, request, env);
}

// ═══════════════════════════════════════
//  Phase 3: Stripe Webhook
// ═══════════════════════════════════════

async function handleStripeWebhook(request, env) {
  const body = await request.text();
  const sig = request.headers.get('stripe-signature');

  // 简单签名验证 (生产环境建议用更严格的 HMAC 校验)
  // 这里先做基本的 webhook 处理
  if (!sig) {
    return errorResponse('Missing stripe-signature', 400, request, env);
  }

  let event;
  try {
    event = JSON.parse(body);
  } catch {
    return errorResponse('Invalid JSON', 400, request, env);
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const submissionId = session.client_reference_id;

    if (submissionId) {
      // 更新 Supabase
      const supabaseUrl = env.SUPABASE_URL;
      const supabaseKey = env.SUPABASE_SERVICE_KEY;

      await fetch(`${supabaseUrl}/rest/v1/diagnostic_submissions?id=eq.${submissionId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'apikey': supabaseKey,
          'Authorization': `Bearer ${supabaseKey}`,
        },
        body: JSON.stringify({
          payment_status: 'paid',
          payment_provider: 'stripe',
          payment_id: session.payment_intent || session.id,
          paid_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }),
      });
    }
  }

  return jsonResponse({ received: true }, 200, request, env);
}

// ═══════════════════════════════════════
//  Phase 3: 查询支付状态
// ═══════════════════════════════════════

async function handleSubmissionStatus(id, request, env) {
  if (!id || id.length < 10) {
    return errorResponse('无效的 submissionId', 400, request, env);
  }

  const supabaseUrl = env.SUPABASE_URL;
  const supabaseKey = env.SUPABASE_SERVICE_KEY;

  const res = await fetch(
    `${supabaseUrl}/rest/v1/diagnostic_submissions?id=eq.${id}&select=id,payment_status,created_at`,
    {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
      },
    }
  );

  if (!res.ok) {
    return errorResponse('查询失败', 500, request, env);
  }

  const data = await res.json();
  if (data.length === 0) {
    return errorResponse('未找到记录', 404, request, env);
  }

  return jsonResponse({
    submissionId: data[0].id,
    paymentStatus: data[0].payment_status,
    createdAt: data[0].created_at,
  }, 200, request, env);
}
