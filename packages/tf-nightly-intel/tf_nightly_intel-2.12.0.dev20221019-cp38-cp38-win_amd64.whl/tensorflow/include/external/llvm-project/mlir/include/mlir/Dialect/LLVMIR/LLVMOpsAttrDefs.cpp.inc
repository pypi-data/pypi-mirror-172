/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_LIST
#undef GET_ATTRDEF_LIST

::mlir::LLVM::CConvAttr,
::mlir::LLVM::FastmathFlagsAttr,
::mlir::LLVM::LinkageAttr,
::mlir::LLVM::LoopOptionsAttr

#endif  // GET_ATTRDEF_LIST

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES

static ::mlir::OptionalParseResult generatedAttributeParser(::mlir::AsmParser &parser, ::llvm::StringRef *mnemonic, ::mlir::Type type, ::mlir::Attribute &value) {
  return ::mlir::AsmParser::KeywordSwitch<::mlir::OptionalParseResult>(parser)
    .Case(::mlir::LLVM::CConvAttr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::LLVM::CConvAttr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::LLVM::FastmathFlagsAttr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::LLVM::FastmathFlagsAttr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::LLVM::LinkageAttr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::LLVM::LinkageAttr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::LLVM::LoopOptionsAttr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::LLVM::LoopOptionsAttr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Default([&](llvm::StringRef keyword, llvm::SMLoc) {
      *mnemonic = keyword;
      return llvm::None;
    });
}

static ::mlir::LogicalResult generatedAttributePrinter(::mlir::Attribute def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Attribute, ::mlir::LogicalResult>(def)    .Case<::mlir::LLVM::CConvAttr>([&](auto t) {
      printer << ::mlir::LLVM::CConvAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::LLVM::FastmathFlagsAttr>([&](auto t) {
      printer << ::mlir::LLVM::FastmathFlagsAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::LLVM::LinkageAttr>([&](auto t) {
      printer << ::mlir::LLVM::LinkageAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::LLVM::LoopOptionsAttr>([&](auto t) {
      printer << ::mlir::LLVM::LoopOptionsAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace LLVM {
namespace detail {
struct CConvAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<CConv>;
  CConvAttrStorage(CConv CallingConv) : CallingConv(CallingConv) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (CallingConv == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static CConvAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto CallingConv = std::get<0>(tblgenKey);
    return new (allocator.allocate<CConvAttrStorage>()) CConvAttrStorage(CallingConv);
  }

  CConv CallingConv;
};
} // namespace detail
CConvAttr CConvAttr::get(::mlir::MLIRContext *context, CConv CallingConv) {
  return Base::get(context, CallingConv);
}

CConv CConvAttr::getCallingConv() const {
  return getImpl()->CallingConv;
}

} // namespace LLVM
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::LLVM::CConvAttr)
namespace mlir {
namespace LLVM {
namespace detail {
struct FastmathFlagsAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::LLVM::FastmathFlags>;
  FastmathFlagsAttrStorage(::mlir::LLVM::FastmathFlags value) : value(value) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static FastmathFlagsAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<FastmathFlagsAttrStorage>()) FastmathFlagsAttrStorage(value);
  }

  ::mlir::LLVM::FastmathFlags value;
};
} // namespace detail
FastmathFlagsAttr FastmathFlagsAttr::get(::mlir::MLIRContext *context, ::mlir::LLVM::FastmathFlags value) {
  return Base::get(context, value);
}

::mlir::Attribute FastmathFlagsAttr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::LLVM::FastmathFlags> _result_value;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::LLVM::FastmathFlags> {
      ::mlir::LLVM::FastmathFlags flags = {};
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      do {
        if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
          return ::mlir::failure();
        auto maybeEnum = ::mlir::LLVM::symbolizeFastmathFlags(enumKeyword);
        if (!maybeEnum) {
            return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::LLVM::FastmathFlags" << " to be one of: " << "none" << ", " << "nnan" << ", " << "ninf" << ", " << "nsz" << ", " << "arcp" << ", " << "contract" << ", " << "afn" << ", " << "reassoc" << ", " << "fast")};
        }
        flags = flags | *maybeEnum;
      } while(::mlir::succeeded(odsParser.parseOptionalComma()));
      return flags;
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse LLVM_FastmathFlagsAttr parameter 'value' which is to be a `::mlir::LLVM::FastmathFlags`");
    return {};
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_value));
  return FastmathFlagsAttr::get(odsParser.getContext(),
      ::mlir::LLVM::FastmathFlags((*_result_value)));
}

void FastmathFlagsAttr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  odsPrinter << stringifyFastmathFlags(getValue());
  odsPrinter << ">";
}

::mlir::LLVM::FastmathFlags FastmathFlagsAttr::getValue() const {
  return getImpl()->value;
}

} // namespace LLVM
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::LLVM::FastmathFlagsAttr)
namespace mlir {
namespace LLVM {
namespace detail {
struct LinkageAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<linkage::Linkage>;
  LinkageAttrStorage(linkage::Linkage linkage) : linkage(linkage) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (linkage == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static LinkageAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto linkage = std::get<0>(tblgenKey);
    return new (allocator.allocate<LinkageAttrStorage>()) LinkageAttrStorage(linkage);
  }

  linkage::Linkage linkage;
};
} // namespace detail
LinkageAttr LinkageAttr::get(::mlir::MLIRContext *context, linkage::Linkage linkage) {
  return Base::get(context, linkage);
}

linkage::Linkage LinkageAttr::getLinkage() const {
  return getImpl()->linkage;
}

} // namespace LLVM
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::LLVM::LinkageAttr)
namespace mlir {
namespace LLVM {
namespace detail {
struct LoopOptionsAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<std::pair<LoopOptionCase, int64_t>>>;
  LoopOptionsAttrStorage(::llvm::ArrayRef<std::pair<LoopOptionCase, int64_t>> options) : options(options) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (options == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static LoopOptionsAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto options = std::get<0>(tblgenKey);
    options = allocator.copyInto(options);
    return new (allocator.allocate<LoopOptionsAttrStorage>()) LoopOptionsAttrStorage(options);
  }

  ::llvm::ArrayRef<std::pair<LoopOptionCase, int64_t>> options;
};
} // namespace detail
::llvm::ArrayRef<std::pair<LoopOptionCase, int64_t>> LoopOptionsAttr::getOptions() const {
  return getImpl()->options;
}

} // namespace LLVM
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::LLVM::LoopOptionsAttr)
namespace mlir {
namespace LLVM {

/// Parse an attribute registered to this dialect.
::mlir::Attribute LLVMDialect::parseAttribute(::mlir::DialectAsmParser &parser,
                                      ::mlir::Type type) const {
  ::llvm::SMLoc typeLoc = parser.getCurrentLocation();
  ::llvm::StringRef attrTag;
  {
    ::mlir::Attribute attr;
    auto parseResult = generatedAttributeParser(parser, &attrTag, type, attr);
    if (parseResult.has_value())
      return attr;
  }
  
  parser.emitError(typeLoc) << "unknown attribute `"
      << attrTag << "` in dialect `" << getNamespace() << "`";
  return {};
}
/// Print an attribute registered to this dialect.
void LLVMDialect::printAttribute(::mlir::Attribute attr,
                         ::mlir::DialectAsmPrinter &printer) const {
  if (::mlir::succeeded(generatedAttributePrinter(attr, printer)))
    return;
  
}
} // namespace LLVM
} // namespace mlir

#endif  // GET_ATTRDEF_CLASSES

