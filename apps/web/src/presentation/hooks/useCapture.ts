"use client";

import { useState } from "react";
import {
	type CaptureConfig,
	defaultCaptureConfig,
} from "@/domain/models/capture";
import { captureClient } from "@/infrastructure/api/client";

export function useCapture() {
	const [config, setConfig] = useState<CaptureConfig>(defaultCaptureConfig());

	const updateConfig = <K extends keyof CaptureConfig>(
		key: K,
		value: CaptureConfig[K],
	) => {
		setConfig((prev: CaptureConfig) => ({ ...prev, [key]: value }));
	};

	const startCapture = async () => {
		if (!config.targetWindowTitle) {
			alert("対象のウィンドウを選択してください");
			return;
		}
		try {
			await captureClient.startCapture(config);
			alert(
				"キャプチャを開始しました。完了すると outputs フォルダに PDF が保存されます（他のアプリを操作しても止まりません）",
			);
		} catch (e) {
			alert(`エラー: ${e instanceof Error ? e.message : e}`);
		}
	};

	return {
		config,
		updateConfig,
		startCapture,
	};
}
