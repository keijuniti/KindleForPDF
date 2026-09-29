"use client";

import { Monitor } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { captureClient } from "@/infrastructure/api/client";

interface WindowPickerProps {
	value: string;
	onChange: (value: string) => void;
}

export function WindowPicker({ value, onChange }: WindowPickerProps) {
	const [error, setError] = useState<string | null>(null);
	// value (ラベル) は裏で保持し、テキストボックスにはアプリ名だけを表示する
	const [picked, setPicked] = useState<{ label: string; name: string } | null>(
		null,
	);

	const pickWindow = async () => {
		setError(null);
		try {
			const stream = await navigator.mediaDevices.getDisplayMedia({
				video: true,
			});
			// ラベル ("window:<CGWindowID>:0") をそのまま渡し、どのアプリかの特定はバックエンドに任せる
			const label = stream.getVideoTracks()[0]?.label ?? "";
			// 欲しいのはラベルだけなので、すぐに共有を止める (撮影はバックエンドが行う)
			for (const track of stream.getTracks()) track.stop();
			if (label) {
				onChange(label);
				setPicked({ label, name: "選択したウィンドウ" });
				// 名前は表示用のみ。取得できなくても (例: クラウド上の BE) キャプチャはラベルで動く
				captureClient
					.getWindowName(label)
					.then((name) =>
						setPicked((prev) =>
							prev?.label === label ? { label, name } : prev,
						),
					)
					.catch(() => {});
			}
		} catch (err) {
			if (err instanceof Error && err.name === "NotAllowedError") {
				setError("ウィンドウの選択がキャンセルされました");
			} else {
				setError("ウィンドウの選択に失敗しました");
			}
		}
	};

	return (
		<div className="space-y-3">
			<div className="flex items-center gap-2">
				<Button type="button" onClick={pickWindow} className="shrink-0">
					<Monitor className="h-4 w-4" />
					ウィンドウを選択
				</Button>
				<Input
					id="window-select"
					type="text"
					placeholder="「ウィンドウを選択」で選ぶか、アプリ名 (例: Kindle) を直接入力してください"
					value={picked?.label === value ? picked.name : value}
					onChange={(e) => onChange(e.target.value)}
				/>
			</div>
			{error && <p className="text-sm text-destructive">{error}</p>}
		</div>
	);
}
