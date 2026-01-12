/**
 * Tipos compartidos para componentes del Kanban
 */

export type CardListID = 1 | 2 | 3;
export type LabelColor = "blue" | "red" | "green" | "yellow" | "purple" | "pink" | "orange" | "indigo";

export interface Label {
  id: string;
  name: string;
  color: LabelColor;
}

export interface ChecklistItem {
  id: string;
  text: string;
  done: boolean;
}

export interface Card {
  id: number;
  title: string;
  description?: string | null;
  due_date?: string | null;
  list_id: CardListID;
  board_id: number;
  labels?: Label[];
  checklist?: ChecklistItem[];
  assignee_id?: string | null;
}

export interface TeamMember {
  id: string;
  name: string;
  avatar?: string;
}

export interface CardFormData {
  title: string;
  description: string;
  due_date: string;
  list_id: CardListID;
  labels: Label[];
  checklist: ChecklistItem[];
  assignee_id: string | null;
}
