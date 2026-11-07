import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
  let req = VNRecognizeTextRequest(); req.recognitionLanguages = ["ja-JP"]; req.recognitionLevel = .accurate; req.usesLanguageCorrection = false
  try? VNImageRequestHandler(cgImage: cg).perform([req])
  for o in (req.results ?? []) { if let c = o.topCandidates(1).first {
    print("\(path)\t\(String(format: "%.4f", 1.0 - o.boundingBox.midY))\t\(c.string)") } }
}
