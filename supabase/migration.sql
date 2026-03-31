-- ═══════════════════════════════════════════
--  曼妮新娘 诊断系统 — Supabase 建表脚本
--  在 Supabase Dashboard → SQL Editor 中运行
-- ═══════════════════════════════════════════

CREATE TABLE IF NOT EXISTS diagnostic_submissions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Step 1: 基础信息
  user_name TEXT NOT NULL,
  user_wechat TEXT NOT NULL,
  user_job TEXT,
  user_age TEXT,

  -- Step 2: 平台与目标
  platform TEXT,
  goals TEXT[] DEFAULT '{}',
  pain_point TEXT,

  -- Step 3: 风格与图片
  styles TEXT[] DEFAULT '{}',
  personal_photos JSONB DEFAULT '[]'::jsonb,
  ref_photos JSONB DEFAULT '[]'::jsonb,

  -- Step 4: 方向与备注
  direction TEXT,
  user_note TEXT,

  -- 支付 (Phase 3)
  payment_status TEXT DEFAULT 'pending',
  payment_provider TEXT,
  payment_id TEXT,
  payment_amount INTEGER DEFAULT 2900,
  paid_at TIMESTAMPTZ,

  -- 扩展预留 (Phase 4)
  openclaw_data JSONB,
  wechat_status TEXT,
  wechat_user_id TEXT,

  -- 系统字段
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  ip_address TEXT,
  user_agent TEXT
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_submissions_wechat ON diagnostic_submissions(user_wechat);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON diagnostic_submissions(payment_status);
CREATE INDEX IF NOT EXISTS idx_submissions_created ON diagnostic_submissions(created_at DESC);

-- RLS: 禁止前端直接访问 (仅 service_role key 可用)
ALTER TABLE diagnostic_submissions ENABLE ROW LEVEL SECURITY;

-- 允许 service_role 全部操作
CREATE POLICY "service_role_all" ON diagnostic_submissions
  FOR ALL
  USING (true)
  WITH CHECK (true);
