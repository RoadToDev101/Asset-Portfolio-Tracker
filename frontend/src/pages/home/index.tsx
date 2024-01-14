import Hero from "./Hero";
import TopCryptoSection from "./TopCryptoSection";
import TopNews from "./TopNewsSection";
import Footer from "@components/shared/Footer";
import ErrorBoundary from "@components/ErrorBoundary";
import PublicHeader from "@/components/shared/PublicHeader";

function Home() {
  return (
    <>
      <PublicHeader />
      <Hero />
      <ErrorBoundary>
        <TopCryptoSection />
      </ErrorBoundary>
      <ErrorBoundary>
        <TopNews />
      </ErrorBoundary>
      <Footer />
    </>
  );
}

export default Home;
