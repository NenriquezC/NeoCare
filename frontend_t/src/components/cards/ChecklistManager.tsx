import React, { useState } from "react";

export interface ChecklistItem {
  id: string;
  title: string;
  done: boolean;
}

interface ChecklistManagerProps {
  items: ChecklistItem[];
  onAddItem: (item: ChecklistItem) => void;
  onToggleItem: (itemId: string) => void;
  onRemoveItem: (itemId: string) => void;
}

export function ChecklistManager({
  items,
  onAddItem,
  onToggleItem,
  onRemoveItem,
}: ChecklistManagerProps) {
  const [newItem, setNewItem] = useState("");

  const handleAdd = () => {
    if (newItem.trim()) {
      onAddItem({
        id: `item-${Date.now()}`,
        title: newItem,
        done: false,
      });
      setNewItem("");
    }
  };

  const progress =
    items.length > 0
      ? Math.round((items.filter((i) => i.done).length / items.length) * 100)
      : 0;

  return (
    <div className="space-y-3">
      {items.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-gray-700">Progreso</span>
            <span className="text-gray-600 font-semibold">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-green-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      <div className="space-y-2">
        {items.map((item) => (
          <div
            key={item.id}
            className="flex items-center gap-3 p-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <input
              type="checkbox"
              checked={item.done}
              onChange={() => onToggleItem(item.id)}
              className="w-4 h-4 cursor-pointer"
            />
            <span
              className={`flex-1 text-sm ${
                item.done
                  ? "line-through text-gray-400"
                  : "text-gray-700"
              }`}
            >
              {item.title}
            </span>
            <button
              onClick={() => onRemoveItem(item.id)}
              className="text-gray-400 hover:text-red-600 transition-colors"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleAdd()}
          placeholder="Nueva subtarea…"
          className="flex-1 px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none text-sm"
        />
        <button
          onClick={handleAdd}
          className="px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium text-sm"
        >
          +
        </button>
      </div>
    </div>
  );
}