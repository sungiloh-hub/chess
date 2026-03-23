import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chess Tutor - 체스 학습 게임",
  description: "체스를 배우면서 전략을 익히는 학습 게임",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
