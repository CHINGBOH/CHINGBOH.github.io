export const metadata = {
  title: '梁清波 · 个人履历与专业作品集 | 懂经营的数字化实干家',
  description:
    '梁清波 (Boone Liang) 个人履历与专业作品集：华中科技大学统计学理学学士，全资子公司从 0 到 1 创办奠基，大宗商业工程总操盘（135 份合同 6.83 亿），上市公司合规与信息披露 A 级；善用数据、报表与 AI 工具为生意提效降本，熟悉各类数据处理与统计工具。',
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
