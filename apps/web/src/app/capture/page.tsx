"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { WindowPicker } from "@/components/window-picker";
import { useCapture } from "@/presentation/hooks/useCapture";

export default function CapturePage() {
	const { config, updateConfig, startCapture } = useCapture();

	return (
		<main className="min-h-screen bg-gradient-to-br from-background via-background to-accent/5 p-4 sm:p-8 lg:p-10">
			<div className="container mx-auto max-w-2xl">
				<Card className="w-full">
					<CardHeader>
						<CardTitle className="text-center">Kindle to PDF Capture</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-3">
							<Label htmlFor="window-select">対象アプリケーション</Label>
							<WindowPicker
								value={config.targetWindowTitle}
								onChange={(value) => updateConfig("targetWindowTitle", value)}
							/>
						</div>
						<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
							<div className="space-y-3">
								<Label htmlFor="pages">総ページ数</Label>
								<Input
									id="pages"
									type="number"
									value={config.pageCount}
									onChange={(e) =>
										updateConfig("pageCount", Number(e.target.value))
									}
								/>
							</div>
							<div className="space-y-3">
								<Label htmlFor="interval">待機時間 (秒)</Label>
								<Input
									id="interval"
									type="number"
									step="0.1"
									value={config.interval}
									onChange={(e) =>
										updateConfig("interval", Number(e.target.value))
									}
								/>
							</div>
						</div>

						<div className="space-y-3">
							<Label htmlFor="filename">保存ファイル名</Label>
							<Input
								id="filename"
								type="text"
								value={config.outputFilename}
								onChange={(e) => updateConfig("outputFilename", e.target.value)}
							/>
						</div>

						<Button
							className="w-full"
							size="lg"
							onClick={startCapture}
							disabled={!config.targetWindowTitle}
						>
							キャプチャ実行開始
						</Button>
					</CardContent>
				</Card>
			</div>
		</main>
	);
}
