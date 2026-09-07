export const metadata = {
  title: '梁清波 · 个人履历与专业作品集 | 全资子公司初创奠基 · 大宗商业工程总操盘 · 数字化解决方案顾问 · 华中科技大学统计学',
  description:
    '梁清波 (Boone Liang) 个人履历与专业作品集：华中科技大学统计学理学学士，全资子公司从 0 到 1 创办奠基，大宗商业工程总操盘（135 份合同 6.83 亿），数字化解决方案顾问，以 VIBE+ 敏捷研发（LLM×Harness 支点 + Context 杠杆）一人覆盖 8 大自研系统、2,804 万行源码。',
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aaaakshat/cm-web-fonts@master/fonts.css" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Noto+Serif+SC:wght@400;500;600;700;900&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
