import React from "react";
import { useParams } from "react-router-dom";
import CardsBoard from "../components/cards/CardsBoard";

export default function KanbanBoard() {
  const { boardId } = useParams<{ boardId: string }>();
  const id = boardId ? parseInt(boardId, 10) : 1;

  return (
    <div className="w-full h-screen overflow-hidden">
      <CardsBoard boardId={id} />
    </div>
  );
}
