import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-purple-500 to-pink-500">
      <div className="text-center p-6 bg-white rounded-lg shadow-xl">
        <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-pink-500">
          404
        </h1>{" "}
        <p className="text-xl mt-4 font-semibold text-gray-700">
          Oops! Digital Drift?
        </p>
        <p className="mt-4 text-gray-600">
          It seems like the crypto wave carried you too far. The page you're
          looking for is in uncharted territory.
        </p>
        <Link
          className="mt-6 inline-block bg-purple-600 text-white px-6 py-3 rounded hover:bg-pink-500 transition duration-300"
          href="/"
        >
          Teleport Back Home
        </Link>
      </div>
    </div>
  );
}
