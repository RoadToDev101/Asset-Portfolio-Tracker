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

const registrationFormSchema = z
  .object({
    username: z.string().min(3).max(50),
    email: z.string().email(),
    password: z.string().min(8).max(100),
    confirmPassword: z.string().min(8),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match.",
    path: ["confirmPassword"],
  })
  .refine((data) => data.username && data.email && data.password, {
    message: "Please fill out all fields.",
    path: ["username", "email", "password"],
  });

export default function Register() {
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const form = useForm<z.infer<typeof registrationFormSchema>>({
    resolver: zodResolver(registrationFormSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const handleRegister = async (
    values: z.infer<typeof registrationFormSchema>
  ) => {
    // Reset error and message
    setError("");
    setMessage("");

    if (values.password !== values.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

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
      const response = await fetch(
        "http://localhost:8000/api/v1/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
          },
          body: formBody,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "An error occurred. Please try again.");
      }

      setMessage(
        "Registration successful! Please check your email to confirm."
      );
      // Handle registration success logic here
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-green-500 via-blue-500 to-purple-500">
      <div className="w-full max-w-md p-8 bg-white shadow-md rounded-lg">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleRegister)}
            className="space-y-8"
          >
            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500 text-center mb-6">
              Register for CryptoTracker
            </h2>
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => {
                return (
                  <FormItem>
                    <FormLabel>User Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Username" type="string" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => {
                return (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input placeholder="Email" type="email" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => {
                return (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Password"
                        type="password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
            <FormField
              control={form.control}
              name="confirmPassword"
              render={({ field }) => {
                return (
                  <FormItem>
                    <FormLabel>Confirm Password</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Confirm Password"
                        type="password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
            <Button
              className="w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              Register
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
            className="font-bold text-sm text-green-500 hover:text-green-800"
            href="/login"
          >
            Already have an account? Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
