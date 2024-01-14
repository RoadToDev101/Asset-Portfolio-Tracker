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

const registrationFormSchema = z
  .object({
    username: z.string().min(3).max(50),
    email: z.string().email(),
    password: z.string().min(8).max(100),
    confirmPassword: z.string().min(8).max(100),
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
  const { performLogin } = useContext(AuthContext);

  const form = useForm<z.infer<typeof registrationFormSchema>>({
    resolver: zodResolver(registrationFormSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const handleRegister = async (values: {
    username: string;
    email: string;
    password: string;
  }) => {
    setError("");
    setMessage("");

    // Prepare form body
    const formBody = JSON.stringify({
      username: values.username,
      email: values.email,
      password: values.password,
    });

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/v1/auth/register`,
        formBody,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setMessage("Registration successful! Redirecting...");
      // Perform login after 1.5 seconds
      setTimeout(() => {
        performLogin(
          response.data.access_token,
          response.data.user_id.toString(),
          response.data.role.toString(),
          response.data.is_active
        );
      }, 3000);
    } catch (err) {
      handleError(err);
    }
  };

  const handleError = (err: unknown) => {
    if (axios.isAxiosError(err) && err.response) {
      setError(
        err.response.data.detail || "An error occurred during registration."
      );
    } else {
      setError("Network error, please try again later.");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-green-500 via-blue-500 to-purple-500">
      <div className="w-full max-w-md p-4 bg-white shadow-md rounded-lg">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleRegister)}
            className="space-y-4"
          >
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
            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500 text-center mb-6">
              Register for Portfolio Tracker
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
        <div className="text-center font-semibold mt-4">
          {error && <p className="text-red-500 text-xs">{error}</p>}
          {message && <p className="text-green-500 text-xs">{message}</p>}
        </div>
        <div className="text-center mt-6">
          <Link
            className="font-bold text-sm text-green-500 hover:text-green-800"
            to="/login"
          >
            Already have an account? Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
