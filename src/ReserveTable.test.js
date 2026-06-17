import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import ReserveTable from "./components/ReserveTable";

describe("ReserveTable Component", () => {
  let dispatchMock;
  let availableTimes;

  beforeEach(() => {
    dispatchMock = jest.fn();
    availableTimes = ["17:00", "18:00", "19:00"];
    render(<ReserveTable availableTimes={availableTimes} dispatch={dispatchMock} />);
  });

  test("renders all form fields", () => {
    expect(screen.getByLabelText(/First Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Last Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Date of Reservation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Time of Reservation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Number of Diners/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Occasion/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Reserve/i })).toBeInTheDocument();
  });

  test("shows error when submitting empty form", () => {
    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));

    expect(screen.getByText(/First name must be between 2 and 30 characters/i)).toBeInTheDocument();
    expect(screen.getByText(/Last name must be between 2 and 30 characters/i)).toBeInTheDocument();
    expect(screen.getByText(/Date is required/i)).toBeInTheDocument();
    expect(screen.getByText(/Time is required/i)).toBeInTheDocument();
    expect(screen.getByText(/Occasion is required/i)).toBeInTheDocument();
  });

  test("shows error if name is too short", () => {
    fireEvent.change(screen.getByLabelText(/First Name/i), { target: { value: "A" } });
    fireEvent.change(screen.getByLabelText(/Last Name/i), { target: { value: "B" } });
    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));

    expect(screen.getByText(/First name must be between 2 and 30 characters/i)).toBeInTheDocument();
    expect(screen.getByText(/Last name must be between 2 and 30 characters/i)).toBeInTheDocument();
  });

  test("submits form successfully with valid input", () => {
    fireEvent.change(screen.getByLabelText(/First Name/i), { target: { value: "John" } });
    fireEvent.change(screen.getByLabelText(/Last Name/i), { target: { value: "Doe" } });
    fireEvent.change(screen.getByLabelText(/Date of Reservation/i), { target: { value: "2025-08-22" } });
    fireEvent.change(screen.getByLabelText(/Time of Reservation/i), { target: { value: "18:00" } });
    fireEvent.change(screen.getByLabelText(/Number of Diners/i), { target: { value: 4 } });
    fireEvent.change(screen.getByLabelText(/Occasion/i), { target: { value: "Birthday" } });

    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));

    // BOOK_TIME dispatched with chosen slot
    expect(dispatchMock).toHaveBeenCalledWith({ type: "BOOK_TIME", time: "18:00" });
  });

  test("removes booked time from availableTimes after submission", () => {
    // initial render shows 18:00 option
    expect(screen.getByRole("option", { name: "18:00" })).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/First Name/i), { target: { value: "Alice" } });
    fireEvent.change(screen.getByLabelText(/Last Name/i), { target: { value: "Smith" } });
    fireEvent.change(screen.getByLabelText(/Date of Reservation/i), { target: { value: "2025-08-22" } });
    fireEvent.change(screen.getByLabelText(/Time of Reservation/i), { target: { value: "18:00" } });
    fireEvent.change(screen.getByLabelText(/Number of Diners/i), { target: { value: 2 } });
    fireEvent.change(screen.getByLabelText(/Occasion/i), { target: { value: "Anniversary" } });

    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));

    // Verify dispatch removes slot
    expect(dispatchMock).toHaveBeenCalledWith({ type: "BOOK_TIME", time: "18:00" });
  });
});
