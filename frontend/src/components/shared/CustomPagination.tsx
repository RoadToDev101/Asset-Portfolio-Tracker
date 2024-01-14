import React from "react";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@ui/pagination";

interface CustomPaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const MAX_PAGE_DISPLAY = 5; // Number of page links to display
const HALF_MAX_DISPLAY = Math.floor(MAX_PAGE_DISPLAY / 2);

const CustomPagination: React.FC<CustomPaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  // Determine the range of page numbers to display
  let startPage = Math.max(1, currentPage - HALF_MAX_DISPLAY);
  let endPage = Math.min(totalPages, currentPage + HALF_MAX_DISPLAY);

  // Adjust the range if near the start or end
  if (currentPage <= HALF_MAX_DISPLAY) {
    endPage = Math.min(MAX_PAGE_DISPLAY, totalPages);
  } else if (currentPage > totalPages - HALF_MAX_DISPLAY) {
    startPage = Math.max(1, totalPages - MAX_PAGE_DISPLAY + 1);
  }

  return (
    <Pagination>
      <PaginationContent>
        {currentPage > 1 && (
          <PaginationPrevious
            href="#"
            onClick={(e) => {
              e.preventDefault();
              onPageChange(currentPage - 1);
            }}
          />
        )}
        {startPage > 1 && (
          <>
            <PaginationLink
              href="#"
              onClick={(e) => {
                e.preventDefault();
                onPageChange(1);
              }}
            >
              1
            </PaginationLink>
            {startPage > 2 && <PaginationEllipsis />}
          </>
        )}
        {Array.from({ length: endPage - startPage + 1 }, (_, index) => (
          <PaginationLink
            key={index}
            href="#"
            onClick={(e) => {
              e.preventDefault();
              onPageChange(index + 1);
            }}
            isActive={currentPage === index + 1}
          >
            {startPage + index}
          </PaginationLink>
        ))}
        {endPage < totalPages && (
          <>
            <PaginationEllipsis />
            <PaginationLink
              href="#"
              onClick={(e) => {
                e.preventDefault();
                onPageChange(totalPages);
              }}
            >
              {totalPages}
            </PaginationLink>
          </>
        )}
        {currentPage < totalPages && (
          <PaginationNext
            href="#"
            onClick={(e) => {
              e.preventDefault();
              onPageChange(currentPage + 1);
            }}
          />
        )}
      </PaginationContent>
    </Pagination>
  );
};

export default CustomPagination;
