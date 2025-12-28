// frontend_t/src/components/layout/AppLayout.tsx
import React from "react";

type Props = {
    children: React.ReactNode;
};

export default function AppLayout({ children }: Props) {
    return (
    <div className="app-bg">
        <div className="app-shell">{children}</div>
    </div>
    );
}