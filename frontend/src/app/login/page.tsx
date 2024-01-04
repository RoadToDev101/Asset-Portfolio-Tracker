"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { useState } from "react";

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

const loginFormSchema = z
  .object({
    username: z.string().min(3).max(20),
    password: z.string().min(6).max(100),
  })
  .refine((data) => data.username && data.password, {
    message: "Please enter your username and password.",
    path: ["username", "password"],
  });

export default function Login() {
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const form = useForm<z.infer<typeof loginFormSchema>>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const handleLogin = async (values: z.infer<typeof loginFormSchema>) => {
    // Reset error and message
    setError("");
    setMessage("");

    // Prepare data for x-www-form-urlencoded
    const formBody = Object.keys(values)
      .map(
        (key) =>
          encodeURIComponent(key) +
          "=" +
          encodeURIComponent(values[key as keyof typeof values])
      )
      .join("&");

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
        body: formBody,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "An error occurred. Please try again.");
      }

      setMessage(data.message);
      // Handle login success logic here, e.g., saving the access token
      console.log("Access Token:", data.access_token);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
      <div className="w-full max-w-md p-8 bg-white shadow-md rounded-lg">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleLogin)} className="space-y-8">
            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500 text-center mb-6">
              Login to CryptoTracker
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
            href="/register"
          >
            Need an account? Register
          </Link>
        </div>
      </div>
    </div>
  );
}
