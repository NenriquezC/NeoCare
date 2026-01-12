import React from "react";
import CardsBoard from "../components/cards/CardsBoard";

export default function BoardPage() {
  // Obtener el boardId de la URL o usar uno por defecto
  const boardId = 1;

  return (
    <div className="w-full h-screen">
      <CardsBoard boardId={boardId} />
    </div>
  );
}
