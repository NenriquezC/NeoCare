import React, { useState } from "react";

export type LabelColor =
  | "red"
  | "blue"
  | "green"
  | "yellow"
  | "purple"
  | "pink"
  | "orange"
  | "indigo";

export interface Label {
  id: string;
  name: string;
  color: LabelColor;
}

const COLOR_CLASSES: Record<LabelColor, string> = {
  red: "bg-red-100 text-red-800 border-red-300",
  blue: "bg-blue-100 text-blue-800 border-blue-300",
  green: "bg-green-100 text-green-800 border-green-300",
  yellow: "bg-yellow-100 text-yellow-800 border-yellow-300",
  purple: "bg-purple-100 text-purple-800 border-purple-300",
  pink: "bg-pink-100 text-pink-800 border-pink-300",
  orange: "bg-orange-100 text-orange-800 border-orange-300",
  indigo: "bg-indigo-100 text-indigo-800 border-indigo-300",
};

interface LabelManagerProps {
  labels: Label[];
  onAddLabel: (label: Label) => void;
  onRemoveLabel: (labelId: string) => void;
  presetLabels: Label[];
}

export function LabelManager({
  labels,
  onAddLabel,
  onRemoveLabel,
  presetLabels,
}: LabelManagerProps) {
  const [showDropdown, setShowDropdown] = useState(false);

  const availableLabels = presetLabels.filter(
    (p) => !labels.find((l) => l.id === p.id)
  );

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {labels.length === 0 ? (
          <p className="text-sm text-gray-500">Sin etiquetas</p>
        ) : (
          labels.map((label) => (
            <div
              key={label.id}
              className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium border ${
                COLOR_CLASSES[label.color]
              }`}
            >
              <span>{label.name}</span>
              <button
                onClick={() => onRemoveLabel(label.id)}
                className="hover:opacity-70 transition-opacity"
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>

      {availableLabels.length > 0 && (
        <div className="relative">
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors flex items-center gap-2"
          >
            <span>+ Añadir etiqueta</span>
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>

          {showDropdown && (
            <div className="absolute z-10 mt-1 w-48 bg-white border border-gray-300 rounded-lg shadow-lg">
              {availableLabels.map((label) => (
                <button
                  key={label.id}
                  onClick={() => {
                    onAddLabel(label);
                    setShowDropdown(false);
                  }}
                  className={`w-full text-left px-4 py-2 hover:bg-gray-100 text-sm border-l-4 ${
                    COLOR_CLASSES[label.color].split(" ")[0]
                  }`}
                >
                  {label.name}
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}