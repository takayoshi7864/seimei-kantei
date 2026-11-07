import Foundation
import CoreServices
for s in CommandLine.arguments.dropFirst() {
  let ns = s as NSString
  if let d = DCSCopyTextDefinition(nil, ns, CFRangeMake(0, ns.length)) {
    let t = d.takeRetainedValue() as String
    print(s, "=>", String(t.prefix(160)).replacingOccurrences(of: "\n", with: " "))
  } else { print(s, "=> none") }
}
