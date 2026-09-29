/**
 * キャプチャ設定の型定義
 */
export interface CaptureConfig {
	pageCount: number;
	interval: number;
	useGrayscale: boolean;
	resizeFactor: number;
	outputFilename: string;
	targetWindowTitle: string;
}

/**
 * CaptureConfigの初期状態を提供する
 */
export const defaultCaptureConfig = (): CaptureConfig => ({
	pageCount: 50,
	interval: 1.5,
	useGrayscale: false,
	resizeFactor: 1.0,
	outputFilename: "captured_book.pdf",
	targetWindowTitle: "",
});
