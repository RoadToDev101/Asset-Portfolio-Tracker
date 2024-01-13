import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@ui/dialog";
import { Input } from "@ui/input";
import { Button } from "@ui/button";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@ui/form";
import axiosInstance from "@/api/axiosInstance";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useContext, useState } from "react";
import { AuthContext } from "@/context/AuthProvider";

const portfolioCreateFormSchema = z.object({
  name: z
    .string({ required_error: "Please enter a portfolio name." })
    .min(3)
    .max(50),
  description: z.string().min(3).max(100),
  asset_type: z
    .string({ required_error: "Please select an asset type." })
    .min(3)
    .max(50),
  user_id: z.string().min(3).max(100),
});

interface PortfolioCreateDialogProps {
  onSuccess?: () => void;
}

const PortfolioCreateDialog = ({ onSuccess }: PortfolioCreateDialogProps) => {
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const { authState } = useContext(AuthContext);

  const form = useForm<z.infer<typeof portfolioCreateFormSchema>>({
    resolver: zodResolver(portfolioCreateFormSchema),
    defaultValues: {
      name: "",
      description: "",
      asset_type: "",
      user_id: authState.user_id || "",
    },
  });

  const handleCreatePortfolio = async (values: {
    name: string;
    description: string;
    asset_type: string;
    user_id: string;
  }) => {
    setError("");
    setMessage("");
    try {
      const response = await axiosInstance.post(`/v1/portfolios`, values);
      if (response.data && response.data.success) {
        setMessage(response.data.message);
        form.reset();
        if (onSuccess) {
          onSuccess();
        }
      }
    } catch (error) {
      handleError(error);
    }
  };

  const handleError = (error: unknown) => {
    if (error instanceof Error) {
      setError(error.message);
    } else if (error instanceof Object) {
      setError(JSON.stringify(error));
    } else {
      setError("There was an error. Please try again later.");
    }
  };

  return (
    <div className="flex justify-end mt-8">
      <Dialog>
        <DialogTrigger asChild>
          <Button>Add New Portfolio</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Add New Portfolio</DialogTitle>
          </DialogHeader>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(handleCreatePortfolio)}>
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel htmlFor="portfolio-name">
                      Portfolio Name
                    </FormLabel>
                    <FormControl>
                      <Input placeholder="Portfolio Name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel htmlFor="portfolio-description">
                      Portfolio Description
                    </FormLabel>
                    <FormControl>
                      <Input placeholder="Portfolio Description" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="asset_type"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel htmlFor="portfolio-asset-type">
                      Asset Type
                    </FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select an asset type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="stocks">Stocks</SelectItem>
                        <SelectItem value="crypto">Crypto</SelectItem>
                        <SelectItem value="others">Other</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage>
                      {form.formState.errors.asset_type?.message}
                    </FormMessage>
                  </FormItem>
                )}
              />
              <DialogFooter className="flex justify-between mt-4">
                <DialogClose asChild>
                  <Button
                    className="flex-1 mr-2"
                    variant="outline"
                    type="reset"
                  >
                    Cancel
                  </Button>
                </DialogClose>
                <Button className="flex-1 ml-2" type="submit">
                  Add
                </Button>
              </DialogFooter>
              <div className="text-center mt-4">
                {error && <p className="text-red-500 text-xs">{error}</p>}
                {message && <p className="text-green-500 text-xs">{message}</p>}
              </div>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PortfolioCreateDialog;
