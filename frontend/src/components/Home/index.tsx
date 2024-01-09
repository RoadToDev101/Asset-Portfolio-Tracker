import Header from "@components/shared/Header";
import Hero from "@/components/Home/Hero";
import TopCryptoSection from "@/components/Home/TopCryptoSection";
import TopNews from "@/components/Home/TopNewsSection";
import Footer from "@components/shared/Footer";
import ErrorBoundary from "@components/ErrorBoundary";

function Home() {
  return (
    <>
      <div className="flex flex-col min-h-screen">
        <Header />
        <Hero />
        <ErrorBoundary>
          <TopCryptoSection />
        </ErrorBoundary>
        <ErrorBoundary>
          <TopNews />
        </ErrorBoundary>
        <Footer />
      </div>
    </>
  );
}

export default Home;
