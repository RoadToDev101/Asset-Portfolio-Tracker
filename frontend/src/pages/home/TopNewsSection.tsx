import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardTitle,
  CardFooter,
} from "@ui/card";
import { AspectRatio } from "@ui/aspect-ratio";
import { Button } from "@ui/button";
import { Skeleton } from "@ui/skeleton";
import { Link } from "react-router-dom";

interface Article {
  source: {
    id: string;
    name: string;
  };
  author: string;
  title: string;
  description: string;
  url: string;
  urlToImage: string;
  publishedAt: string;
  content: string;
}

const TopNewsSection = () => {
  const [news, setNews] = useState<Article[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    // Data is stale if older than 15 minutes
    const isDataStale = (timestamp: number) => {
      return new Date().getTime() - timestamp > 15 * 60 * 1000;
    };

    // Save the data to localStorage
    const saveToLocalStorage = (data: Article[]) => {
      const dataWithTimestamp = {
        timestamp: new Date().getTime(),
        data: data,
      };
      localStorage.setItem("breakingNews", JSON.stringify(dataWithTimestamp));
    };

    const fetchBreakingNews = async (retryCount = 0) => {
      try {
        // Check if the data is in localStorage
        const cachedData = localStorage.getItem("breakingNews");
        const cachedObject = cachedData ? JSON.parse(cachedData) : null;
        if (cachedObject && !isDataStale(cachedObject.timestamp)) {
          setNews(cachedObject.data);
          return;
        }

        const response = await fetch(
          `https://newsapi.org/v2/everything?q=crypto+OR+ethereum+OR+bitcoin&language=en&sortBy=publishedAt&pageSize=3&apiKey=${
            import.meta.env.VITE_NEWS_API_KEY
          }`,
          { signal }
        );

        if (!response.ok) {
          if (response.status === 429 && retryCount < 3) {
            // We hit the rate limit, retry after 1 minute
            setTimeout(
              () => fetchBreakingNews(retryCount + 1),
              Math.pow(2, retryCount) * 1000
            );
            return;
          }
          throw new Error("API request failed");
        }
        const data = await response.json();
        setNews(data.articles);
        saveToLocalStorage(data.articles);
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }
        console.error(error);
        if (retryCount < 3) {
          setTimeout(
            () => fetchBreakingNews(retryCount + 1),
            Math.pow(2, retryCount) * 1000
          );
        }
      }
    };

    fetchBreakingNews();
    const intervalId = setInterval(fetchBreakingNews, 15 * 60 * 1000); // 15 minutes

    return () => {
      clearInterval(intervalId);
      controller.abort();
    };
  }, []);

  return (
    <div className="w-full py-12 md:py-24 lg:py-32">
      <div className="grid items-center justify-center gap-4 px-4 text-center md:px-6">
        <div className="space-y-3">
          <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-400">
            Latest Cryptocurrency News
          </h2>
          <p className="mx-auto max-w-[800px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
            Stay informed with the latest news and updates in the cryptocurrency
            world.
          </p>
        </div>
        <div className="mx-auto grid max-w-sm items-start gap-8 sm:max-w-4xl sm:grid-cols-2 md:gap-12 lg:max-w-7xl lg:grid-cols-3">
          {!news.length
            ? Array(3)
                .fill(null)
                .map((_, index) => (
                  <div className="flex items-center space-x-4" key={index}>
                    <Skeleton className="h-24 w-24" />
                    <div className="space-y-2">
                      <Skeleton className="h-4 w-[250px]" />
                      <Skeleton className="h-4 w-[200px]" />
                      <Skeleton className="h-4 w-[150px]" />
                      <Skeleton className="h-4 w-[50px]" />
                    </div>
                  </div>
                ))
            : news.map((article) => (
                <Card
                  key={article.publishedAt}
                  className="flex flex-col bg-white dark:bg-gray-700 hover:shadow-xl h-full rounded-xl overflow-hidden shadow-lg transition-shadow duration-300"
                >
                  <CardHeader className="p-4 border-b dark:border-gray-600 flex flex-col justify-between">
                    <AspectRatio
                      ratio={16 / 9}
                      className="w-full flex-shrink-0"
                    >
                      <img
                        src={
                          article.urlToImage ||
                          "https://placehold.co/500x300.png"
                        }
                        alt={article.title || "News"}
                        className="w-full h-48 object-cover"
                        width={500}
                        height={300}
                      />
                    </AspectRatio>
                    <CardTitle className="text-lg font-bold my-2">
                      {article.title || "Title not available"}
                    </CardTitle>
                  </CardHeader>
                  <div className="flex flex-col justify-between pt-2 px-4 flex-grow">
                    <div>
                      <CardDescription className="text-sm text-gray-700 dark:text-gray-400">
                        {article.description || "Description not available"}
                      </CardDescription>
                    </div>
                    <CardContent>
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block mt-4 text-blue-600 hover:text-blue-800 transition-colors duration-300"
                      >
                        Read more
                      </a>
                      <CardFooter className="text-sm pt-4 justify-center text-gray-500 dark:text-gray-400 mt-2">
                        {article.publishedAt
                          ? new Date(article.publishedAt).toLocaleDateString(
                              "en-US",
                              {
                                year: "numeric",
                                month: "long",
                                day: "numeric",
                                hour: "2-digit",
                                minute: "2-digit",
                              }
                            )
                          : "Date not available"}
                      </CardFooter>
                    </CardContent>
                  </div>
                </Card>
              ))}
        </div>
        <Link to="/news" className="inline-block mt-8">
          <Button className="bg-pink-500 hover:bg-pink-800 text-white font-bold py-2 px-4 rounded">
            Explore All Crypto News
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default TopNewsSection;
