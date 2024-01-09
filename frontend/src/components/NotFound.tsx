const NotFound = () => {
  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-indigo-500 via-purple-400 to-pink-400">
      <div className="text-center p-6 bg-white rounded-lg shadow-xl">
        <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
          404
        </h1>{" "}
        <p className="text-xl mt-4 font-semibold text-gray-700">
          Oops! Page not found.
        </p>
        <p className="mt-4 text-gray-600">
          It seems like you found a glitch in the matrix...
        </p>
        <a
          className="mt-6 inline-block bg-purple-600 text-white px-6 py-3 rounded hover:bg-pink-500 transition duration-300"
          href="/"
        >
          Teleport Back Home
        </a>
      </div>
    </div>
  );
};

export default NotFound;
