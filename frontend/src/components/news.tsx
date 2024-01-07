import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardTitle,
  CardFooter,
} from "@ui/card";
import Image from "next/image";
import { AspectRatio } from "@ui/aspect-ratio";
import Link from "next/link";
import { Button } from "@ui/button";

const NewsSection = () => {
  const [news, setNews] = useState<any[]>([]);

  useEffect(() => {
    const fetchNews = async () => {
      const response = await fetch(
        `https://newsapi.org/v2/everything?q=crypto+OR+ethereum+OR+bitcoin&language=en&sortBy=publishedAt&pageSize=3&apiKey=${process.env.NEXT_PUBLIC_NEWS_API_KEY}`
      );
      const data = await response.json();
      setNews(data.articles);
    };

    fetchNews();

    const intervalId = setInterval(fetchNews, 60000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="w-full py-12 md:py-24 lg:py-32">
      <div className="grid items-center justify-center gap-4 px-4 text-center md:px-6">
        <div className="space-y-3">
          <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
            Latest Cryptocurrency News
          </h2>
          <p className="mx-auto max-w-[800px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
            Stay informed with the latest news and updates in the cryptocurrency
            world.
          </p>
        </div>
        <div className="mx-auto grid max-w-sm items-start gap-8 sm:max-w-4xl sm:grid-cols-2 md:gap-12 lg:max-w-7xl lg:grid-cols-3">
          {news.map((article, index) => (
            <Card
              key={index}
              className="flex flex-col bg-white dark:bg-gray-700 hover:shadow-xl h-full rounded-xl overflow-hidden shadow-lg transition-shadow duration-300"
            >
              <CardHeader className="p-4 border-b dark:border-gray-600 flex flex-col justify-between">
                <AspectRatio ratio={16 / 9} className="w-full flex-shrink-0">
                  <Image
                    src={article.urlToImage || "/placeholder.svg"}
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
        <Link href="/news" className="inline-block mt-8">
          <Button className="bg-pink-500 hover:bg-purple-500 text-white font-bold py-2 px-4 rounded">
            Explore All Crypto News
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default NewsSection;
