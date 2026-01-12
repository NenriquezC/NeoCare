import React, { useState } from "react";
import { type Label, type LabelColor } from "./LabelManager";

const COLOR_CLASSES: Record<LabelColor, string> = {
  red: "bg-red-100 text-red-800 border-red-300 hover:bg-red-200",
  blue: "bg-blue-100 text-blue-800 border-blue-300 hover:bg-blue-200",
  green: "bg-green-100 text-green-800 border-green-300 hover:bg-green-200",
  yellow: "bg-yellow-100 text-yellow-800 border-yellow-300 hover:bg-yellow-200",
  purple: "bg-purple-100 text-purple-800 border-purple-300 hover:bg-purple-200",
  pink: "bg-pink-100 text-pink-800 border-pink-300 hover:bg-pink-200",
  orange: "bg-orange-100 text-orange-800 border-orange-300 hover:bg-orange-200",
  indigo: "bg-indigo-100 text-indigo-800 border-indigo-300 hover:bg-indigo-200",
};

interface LabelFilterProps {
  selectedLabels: string[];
  onLabelToggle: (labelId: string) => void;
  availableLabels: Label[];
}

export function LabelFilter({
  selectedLabels,
  onLabelToggle,
  availableLabels,
}: LabelFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {availableLabels.map((label) => {
        const isSelected = selectedLabels.includes(label.id);
        return (
          <button
            key={label.id}
            onClick={() => onLabelToggle(label.id)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium border-2 transition-all ${
              isSelected
                ? `${COLOR_CLASSES[label.color]} ring-2 ring-offset-1`
                : "bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200"
            }`}
          >
            {label.name}
            {isSelected && <span className="ml-1">✓</span>}
          </button>
        );
      })}
    </div>
  );
}