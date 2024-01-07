"use client";

import Header from "@components/header";
import HeroSection from "@components/hero";
import TopCryptoSection from "@components/top-crypto";
import NewsSection from "@components/news";
import Footer from "@components/footer";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <HeroSection />
      <TopCryptoSection />
      <NewsSection />
      <Footer />
    </div>
  );
}
