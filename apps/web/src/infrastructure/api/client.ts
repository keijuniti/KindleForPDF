import type { CaptureConfig } from "@/domain/models/capture";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

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
			// detail は HTTPException なら文字列、Pydantic の検証エラーなら配列
			const { detail } = await response.json().catch(() => ({}));
			const message = typeof detail === "string" ? detail : detail?.[0]?.msg;
			throw new Error(message || "キャプチャの開始に失敗しました");
		}

		return response.json();
	},

	/**
	 * ウィンドウのラベル ("window:<id>:0") から表示用のアプリ名を取得
	 */
	async getWindowName(label: string): Promise<string> {
		const response = await fetch(
			`${API_BASE_URL}/window-name?${new URLSearchParams({ label })}`,
		);
		if (!response.ok) {
			throw new Error("アプリ名を取得できませんでした");
		}
		return (await response.json()).name;
	},
};
