import React from "react";
import CardsBoard from "../components/cards/CardsBoard";

export default function KanbanPage() {
  const boardId = 1; // O extraer de URL params si es necesario

  return (
    <div className="w-full h-screen overflow-hidden">
      <CardsBoard boardId={boardId} />
    </div>
  );
}
