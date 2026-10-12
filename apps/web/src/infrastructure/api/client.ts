import type { CaptureConfig } from "@/domain/models/capture";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export interface WindowInfo {
	id: number;
	name: string;
	title: string;
	width: number;
	height: number;
	preview: string | null;
}

// detail は HTTPException なら文字列、Pydantic の検証エラーなら配列
async function errorMessage(
	response: Response,
	fallback: string,
): Promise<string> {
	const { detail } = await response.json().catch(() => ({}));
	return (typeof detail === "string" ? detail : detail?.[0]?.msg) || fallback;
}

export const captureClient = {
	/**
	 * キャプチャ開始リクエストを送信
	 */
	async startCapture(
		config: CaptureConfig,
	): Promise<{ status: string; message: string }> {
		const response = await fetch(`${API_BASE_URL}/capture`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(config),
		});

		if (!response.ok) {
			throw new Error(
				await errorMessage(response, "キャプチャの開始に失敗しました"),
			);
		}

		return response.json();
	},

	/**
	 * APIが検出した撮影候補のウィンドウ一覧 (id が撮影時の識別子)
	 */
	async listWindows(): Promise<WindowInfo[]> {
		const response = await fetch(`${API_BASE_URL}/windows`);
		if (!response.ok) {
			throw new Error(
				await errorMessage(response, "ウィンドウ一覧を取得できませんでした"),
			);
		}
		return response.json();
	},
};
