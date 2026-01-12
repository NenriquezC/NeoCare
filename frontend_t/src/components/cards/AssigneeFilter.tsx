import React, { useState } from "react";

export interface TeamMember {
  id: string;
  name: string;
  avatar: string;
}

interface AssigneeFilterProps {
  selectedAssignee: string | null;
  onAssigneeChange: (assigneeId: string | null) => void;
  teamMembers: TeamMember[];
}

export function AssigneeFilter({
  selectedAssignee,
  onAssigneeChange,
  teamMembers,
}: AssigneeFilterProps) {
  const [showDropdown, setShowDropdown] = useState(false);

  const selectedMember = teamMembers.find((m) => m.id === selectedAssignee);

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="flex items-center gap-2 px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm font-medium"
      >
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
        </svg>
        <span>{selectedMember ? selectedMember.name : "Todos"}</span>
      </button>

      {showDropdown && (
        <div className="absolute z-10 mt-1 w-48 bg-white border border-gray-300 rounded-lg shadow-lg">
          <button
            onClick={() => {
              onAssigneeChange(null);
              setShowDropdown(false);
            }}
            className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 ${
              !selectedAssignee ? "bg-blue-50 font-semibold" : ""
            }`}
          >
            Todos
          </button>

          {teamMembers.map((member) => (
            <button
              key={member.id}
              onClick={() => {
                onAssigneeChange(member.id);
                setShowDropdown(false);
              }}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 flex items-center gap-2 ${
                selectedAssignee === member.id ? "bg-blue-50 font-semibold" : ""
              }`}
            >
              <img
                src={member.avatar}
                alt={member.name}
                className="w-5 h-5 rounded-full"
              />
              {member.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}