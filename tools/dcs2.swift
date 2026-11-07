import Foundation
import CoreServices
let path = CommandLine.arguments[1]
let chars = try! String(contentsOfFile: path, encoding: .utf8).split(separator: "\n").map(String.init)
var out: [String: String] = [:]
for s in chars {
  let ns = s as NSString
  if let d = DCSCopyTextDefinition(nil, ns, CFRangeMake(0, ns.length)) {
    out[s] = String(d.takeRetainedValue() as String)
  }
}
let data = try! JSONSerialization.data(withJSONObject: out, options: [])
try! data.write(to: URL(fileURLWithPath: CommandLine.arguments[2]))
print(out.count)
