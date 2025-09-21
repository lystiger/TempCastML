import React from "react";

export default function About() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">About</h1>
      <p className="bg-white p-4 shadow rounded">
        This project predicts indoor temperature for study purposes.
        Data is currently mocked but will be connected to a real backend later.
      </p>
    </div>
  );
}
