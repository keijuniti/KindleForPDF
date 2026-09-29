// src/app/page.tsx
import { redirect } from "next/navigation";

export default function RootPage() {
	// localhost:3000 にアクセスしたら localhost:3000/capture へ
	redirect("/capture");
}
