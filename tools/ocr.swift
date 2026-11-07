import Foundation
import PDFKit
import Vision
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let s = Int(a[2])!, e = Int(a[3])!
for i in s...min(e, doc.pageCount) {
  guard let p = doc.page(at: i-1) else { continue }
  let r = p.bounds(for: .mediaBox); let sc: CGFloat = 2400 / max(r.width, r.height)
  let img = p.thumbnail(of: NSSize(width: r.width*sc, height: r.height*sc), for: .mediaBox)
  if a.count > 4 { if let t = img.tiffRepresentation, let b = NSBitmapImageRep(data: t), let d = b.representation(using: .png, properties: [:]) { try? d.write(to: URL(fileURLWithPath: "\(a[4])/p\(i).png")) } }
  var cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil)!
  let req = VNRecognizeTextRequest(); req.recognitionLanguages = ["ja-JP"]; req.recognitionLevel = .accurate; req.usesLanguageCorrection = false
  try? VNImageRequestHandler(cgImage: cg).perform([req])
  let obs = (req.results ?? []).sorted { $0.boundingBox.midY > $1.boundingBox.midY }
  print("=== PAGE \(i)")
  for o in obs { if let c = o.topCandidates(1).first { print("\(Int(o.boundingBox.minX*100)),\(Int(o.boundingBox.midY*100)) " + c.string) } }
}
