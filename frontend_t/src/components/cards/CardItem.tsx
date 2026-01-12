import React from "react";
import { Card, Label, ChecklistItem } from "./CardsBoard";
import { LabelColor } from "./LabelManager";

const COLOR_CLASSES: Record<LabelColor, string> = {
  red: "bg-red-100 text-red-800",
  blue: "bg-blue-100 text-blue-800",
  green: "bg-green-100 text-green-800",
  yellow: "bg-yellow-100 text-yellow-800",
  purple: "bg-purple-100 text-purple-800",
  pink: "bg-pink-100 text-pink-800",
  orange: "bg-orange-100 text-orange-800",
  indigo: "bg-indigo-100 text-indigo-800",
};

interface CardItemProps {
  card: Card;
  onEdit: (card: Card) => void;
}

export function CardItem({ card, onEdit }: CardItemProps) {
  const checklistProgress = card.checklist
    ? Math.round(
        (card.checklist.filter((i) => i.done).length / card.checklist.length) *
          100
      )
    : 0;

  const daysUntil = card.due_date
    ? Math.ceil(
        (new Date(card.due_date).getTime() - new Date().getTime()) / 86400000
      )
    : null;

  const getDueBadgeColor = (days: number | null) => {
    if (!days) return "";
    if (days < 0) return "bg-red-600 text-white";
    if (days === 0) return "bg-red-500 text-white";
    if (days <= 3) return "bg-orange-500 text-white";
    return "bg-blue-500 text-white";
  };

  return (
    <button
      onClick={() => onEdit(card)}
      className="w-full text-left bg-white border border-gray-200 rounded-lg p-3 hover:shadow-lg hover:border-blue-300 transition-all duration-200 group"
    >
      {/* TITULO */}
      <h4 className="font-semibold text-gray-900 text-sm mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">
        {card.title}
      </h4>

      {/* DESCRIPCION */}
      {card.description && (
        <p className="text-xs text-gray-600 mb-2 line-clamp-2">
          {card.description}
        </p>
      )}

      {/* ETIQUETAS */}
      {card.labels && card.labels.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {card.labels.map((label) => (
            <span
              key={label.id}
              className={`text-xs px-2 py-1 rounded-full font-medium ${
                COLOR_CLASSES[label.color]
              }`}
            >
              {label.name}
            </span>
          ))}
        </div>
      )}

      {/* CHECKLIST PROGRESS */}
      {card.checklist && card.checklist.length > 0 && (
        <div className="mb-2 space-y-1">
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-600">
              {card.checklist.filter((i) => i.done).length}/{card.checklist.length}
            </span>
            <span className="font-semibold text-gray-700">{checklistProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div
              className="bg-green-500 h-1.5 rounded-full transition-all"
              style={{ width: `${checklistProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* FOOTER: Fecha + Responsable */}
      <div className="flex items-center justify-between text-xs pt-2 border-t border-gray-100">
        {card.due_date ? (
          <span
            className={`px-2 py-1 rounded-md font-medium ${getDueBadgeColor(
              daysUntil
            )}`}
          >
            {daysUntil && daysUntil < 0
              ? `Vencido hace ${Math.abs(daysUntil)} días`
              : daysUntil === 0
              ? "Hoy"
              : `${daysUntil} días`}
          </span>
        ) : (
          <span className="text-gray-400">Sin fecha</span>
        )}

        {card.assignee_id && (
          <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">
            {card.assignee_id.charAt(0).toUpperCase()}
          </div>
        )}
      </div>
    </button>
  );
}