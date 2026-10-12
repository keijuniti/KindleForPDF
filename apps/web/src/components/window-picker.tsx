"use client";

import { Monitor } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { captureClient, type WindowInfo } from "@/infrastructure/api/client";

interface WindowPickerProps {
	value: number | null;
	onChange: (value: number | null) => void;
}

function WindowCard({
	window: w,
	onPick,
}: {
	window: WindowInfo;
	onPick: (w: WindowInfo) => void;
}) {
	return (
		<button
			type="button"
			onClick={() => onPick(w)}
			className="overflow-hidden rounded-lg border bg-card text-left transition hover:border-primary hover:shadow-md"
		>
			<div className="flex aspect-video items-center justify-center bg-muted">
				{/* biome-ignore lint/performance/noImgElement: APIが返すdata URLで next/image は不要 */}
				<img
					src={w.preview ?? undefined}
					alt={w.name}
					className="h-full w-full object-contain"
				/>
			</div>
			<div className="p-2 text-sm">
				<p className="truncate font-medium">{w.title || w.name}</p>
				{w.title && (
					<p className="truncate text-xs text-muted-foreground">{w.name}</p>
				)}
			</div>
		</button>
	);
}

export function WindowPicker({ value, onChange }: WindowPickerProps) {
	const [error, setError] = useState<string | null>(null);
	const [windows, setWindows] = useState<WindowInfo[] | null>(null);
	const [picked, setPicked] = useState<WindowInfo | null>(null);

	// 一覧と識別子 (id) はAPIが検出する。ブラウザ側は選ぶだけ
	const openPicker = async () => {
		setError(null);
		try {
			setWindows(await captureClient.listWindows());
		} catch (e) {
			setWindows(null);
			setError(
				e instanceof Error ? e.message : "ウィンドウ一覧の取得に失敗しました",
			);
		}
	};

	const pick = (w: WindowInfo) => {
		setPicked(w);
		setWindows(null);
		onChange(w.id);
	};

	return (
		<div className="space-y-3">
			<div className="flex items-center gap-2">
				<Button type="button" onClick={openPicker} className="shrink-0">
					<Monitor className="h-4 w-4" />
					ウィンドウを選択
				</Button>
				<Input
					id="window-select"
					type="text"
					readOnly
					placeholder="「ウィンドウを選択」から対象を選んでください"
					value={picked && picked.id === value ? picked.name : ""}
				/>
			</div>
			{error && <p className="text-sm text-destructive">{error}</p>}
			{windows && (
				<div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
					<div className="flex max-h-full w-full max-w-3xl flex-col rounded-xl bg-background p-4 shadow-xl">
						<div className="mb-3 flex items-center justify-between">
							<h2 className="font-semibold">撮影するウィンドウを選択</h2>
							<Button
								type="button"
								variant="ghost"
								size="sm"
								onClick={() => setWindows(null)}
							>
								閉じる
							</Button>
						</div>
						<div className="grid grid-cols-2 gap-3 overflow-y-auto sm:grid-cols-3">
							{windows
								.filter((w) => w.preview)
								.map((w) => (
									<WindowCard key={w.id} window={w} onPick={pick} />
								))}
							{windows.length === 0 && (
								<p className="col-span-full p-3 text-sm text-muted-foreground">
									選択できるウィンドウがありません
								</p>
							)}
						</div>
						{windows.some((w) => !w.preview) && (
							<details className="mt-3 overflow-y-auto">
								<summary className="cursor-pointer text-sm text-muted-foreground">
									その他のウィンドウ (プレビューを取得できないもの)
								</summary>
								<ul className="mt-2 divide-y rounded-md border">
									{windows
										.filter((w) => !w.preview)
										.map((w) => (
											<li key={w.id}>
												<button
													type="button"
													onClick={() => pick(w)}
													className="w-full px-3 py-2 text-left text-sm hover:bg-accent"
												>
													{w.title || w.name}
													{w.title && (
														<span className="ml-2 text-muted-foreground">
															{w.name}
														</span>
													)}
												</button>
											</li>
										))}
								</ul>
							</details>
						)}
					</div>
				</div>
			)}
		</div>
	);
}
