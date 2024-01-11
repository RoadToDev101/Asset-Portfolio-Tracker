import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useState, useContext } from "react";
import axios from "axios";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@ui/form";
import { Button } from "@ui/button";
import { Input } from "@ui/input";
import { AuthContext } from "@/context/AuthProvider";
import { Link } from "react-router-dom";

const loginFormSchema = z
  .object({
    username: z.string().min(3).max(50),
    password: z.string().min(8).max(100),
  })
  .refine((data) => data.username && data.password, {
    message: "Please enter your username and password.",
    path: ["username", "password"],
  });

export default function Login() {
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const { performLogin } = useContext(AuthContext);

  const form = useForm<z.infer<typeof loginFormSchema>>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const handleLogin = async (values: {
    username: string;
    password: string;
  }) => {
    setError("");
    setMessage("");

    const formBody = Object.keys(values)
      .map(
        (key) =>
          encodeURIComponent(key) +
          "=" +
          encodeURIComponent(values[key as keyof typeof values])
      )
      .join("&");

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/v1/auth/login`,
        formBody,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
          },
          withCredentials: true,
        }
      );

      if (response.status === 200 || response.status === 201) {
        setMessage("Login successful! Redirecting to dashboard...");
        performLogin(
          response.data.access_token,
          response.data.user_id.toString()
        );
      }
    } catch (err) {
      handleError(err);
    }
  };

  const handleError = (err: unknown) => {
    if (axios.isAxiosError(err) && err.response) {
      setError(err.response.data.detail || "Login failed. Please try again.");
    } else {
      setError("Network error, please try again later.");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
      <div className="w-full max-w-md p-8 bg-white shadow-md rounded-lg">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleLogin)} className="space-y-8">
            <div className="flex justify-center">
              <Link to="/">
                <img
                  src="/assets/icons/logo.svg"
                  alt="Portfolio Tracker"
                  width={40}
                  height={40}
                />
              </Link>
            </div>
            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500 text-center mb-6">
              Login to Portfolio Tracker
            </h2>
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Username</FormLabel>
                  <FormControl>
                    <Input placeholder="Username" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="Password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button
              className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              Sign In
            </Button>
          </form>
        </Form>
        {/* Error and Success Messages */}
        <div className="text-center mt-4">
          {error && <p className="text-red-500 text-xs">{error}</p>}
          {message && <p className="text-green-500 text-xs">{message}</p>}
        </div>
        <div className="text-center mt-6">
          <Link
            className="font-bold text-sm text-blue-500 hover:text-blue-800"
            to="/register"
          >
            Need an account? Register
          </Link>
        </div>
      </div>
    </div>
  );
}
