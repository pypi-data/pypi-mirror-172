/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
class DestinationStyleOpInterface;
namespace detail {
struct DestinationStyleOpInterfaceInterfaceTraits {
  struct Concept {
    std::pair<int64_t, int64_t> (*getOutputsPositionRange)(const Concept *impl, ::mlir::Operation *);
    int64_t (*getNumOutputs)(const Concept *impl, ::mlir::Operation *);
    OpOperandVector (*getOutputOperands)(const Concept *impl, ::mlir::Operation *);
    OpOperand *(*getOutputOperand)(const Concept *impl, ::mlir::Operation *, int64_t);
    void (*setOutputOperand)(const Concept *impl, ::mlir::Operation *, int64_t, Value);
    int64_t (*getNumInputs)(const Concept *impl, ::mlir::Operation *);
    OpOperandVector (*getInputOperands)(const Concept *impl, ::mlir::Operation *);
    OpOperand *(*getInputOperand)(const Concept *impl, ::mlir::Operation *, int64_t);
    bool (*isInput)(const Concept *impl, ::mlir::Operation *, OpOperand *);
    bool (*isOutput)(const Concept *impl, ::mlir::Operation *, OpOperand *);
    bool (*isScalar)(const Concept *impl, ::mlir::Operation *, OpOperand *);
    OpResult (*getTiedOpResult)(const Concept *impl, ::mlir::Operation *, OpOperand *);
    bool (*hasBufferSemantics)(const Concept *impl, ::mlir::Operation *);
    bool (*hasTensorSemantics)(const Concept *impl, ::mlir::Operation *);
    Operation *(*clone)(const Concept *impl, ::mlir::Operation *, OpBuilder &, Location, TypeRange, ValueRange);
    Operation *(*cloneWithoutRegions)(const Concept *impl, ::mlir::Operation *, OpBuilder &, Location, TypeRange, ValueRange);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::DestinationStyleOpInterface;
    Model() : Concept{getOutputsPositionRange, getNumOutputs, getOutputOperands, getOutputOperand, setOutputOperand, getNumInputs, getInputOperands, getInputOperand, isInput, isOutput, isScalar, getTiedOpResult, hasBufferSemantics, hasTensorSemantics, clone, cloneWithoutRegions} {}

    static inline std::pair<int64_t, int64_t> getOutputsPositionRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline int64_t getNumOutputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperandVector getOutputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperand *getOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i);
    static inline void setOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i, Value value);
    static inline int64_t getNumInputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperandVector getInputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperand *getInputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i);
    static inline bool isInput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline bool isOutput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline bool isScalar(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline OpResult getTiedOpResult(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline bool hasBufferSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool hasTensorSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline Operation *clone(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands);
    static inline Operation *cloneWithoutRegions(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::DestinationStyleOpInterface;
    FallbackModel() : Concept{getOutputsPositionRange, getNumOutputs, getOutputOperands, getOutputOperand, setOutputOperand, getNumInputs, getInputOperands, getInputOperand, isInput, isOutput, isScalar, getTiedOpResult, hasBufferSemantics, hasTensorSemantics, clone, cloneWithoutRegions} {}

    static inline std::pair<int64_t, int64_t> getOutputsPositionRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline int64_t getNumOutputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperandVector getOutputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperand *getOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i);
    static inline void setOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i, Value value);
    static inline int64_t getNumInputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperandVector getInputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline OpOperand *getInputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i);
    static inline bool isInput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline bool isOutput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline bool isScalar(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline OpResult getTiedOpResult(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand);
    static inline bool hasBufferSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool hasTensorSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline Operation *clone(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands);
    static inline Operation *cloneWithoutRegions(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
    int64_t getNumOutputs(::mlir::Operation *tablegen_opaque_val) const;
    OpOperandVector getOutputOperands(::mlir::Operation *tablegen_opaque_val) const;
    OpOperand *getOutputOperand(::mlir::Operation *tablegen_opaque_val, int64_t i) const;
    void setOutputOperand(::mlir::Operation *tablegen_opaque_val, int64_t i, Value value) const;
    int64_t getNumInputs(::mlir::Operation *tablegen_opaque_val) const;
    OpOperandVector getInputOperands(::mlir::Operation *tablegen_opaque_val) const;
    OpOperand *getInputOperand(::mlir::Operation *tablegen_opaque_val, int64_t i) const;
    bool isInput(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const;
    bool isOutput(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const;
    bool isScalar(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const;
    OpResult getTiedOpResult(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const;
    bool hasBufferSemantics(::mlir::Operation *tablegen_opaque_val) const;
    bool hasTensorSemantics(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct DestinationStyleOpInterfaceTrait;

} // namespace detail
class DestinationStyleOpInterface : public ::mlir::OpInterface<DestinationStyleOpInterface, detail::DestinationStyleOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<DestinationStyleOpInterface, detail::DestinationStyleOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::DestinationStyleOpInterfaceTrait<ConcreteOp> {};
  /// Return start and end indices of the output operands range.
  std::pair<int64_t, int64_t> getOutputsPositionRange();
  /// Return the number of outputs.
  int64_t getNumOutputs();
  /// Return the output operands.
  OpOperandVector getOutputOperands();
  /// Return the `i`-th output operand.
  OpOperand *getOutputOperand(int64_t i);
  /// Set the `i`-th output operand.
  void setOutputOperand(int64_t i, Value value);
  /// Return the number of inputs.
  int64_t getNumInputs();
  /// Return the input operands.
  OpOperandVector getInputOperands();
  /// Return the `i`-th input operand.
  OpOperand *getInputOperand(int64_t i);
  /// Return true if `opOperand` is an input.
  bool isInput(OpOperand * opOperand);
  /// Return true if `opOperand` is an output.
  bool isOutput(OpOperand * opOperand);
  /// Return true if the `opOperand` is a scalar value.
  bool isScalar(OpOperand * opOperand);
  /// Return the result tied to `opOperand`.
  OpResult getTiedOpResult(OpOperand * opOperand);
  /// Return whether the op has only MemRef input and outputs.
  bool hasBufferSemantics();
  /// Return whether the op has only RankedTensor input and outputs.
  bool hasTensorSemantics();
  /// Clone the current operation with the given location and operands. This
  /// is used to abstract away the optional underlying region creation. This
  /// does not change the balance between input, output_buffer and
  /// init_tensors operands.
  Operation *clone(OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands);
  /// Clone the current operation with the given location, operands
  /// and BlockAndValueMapping but leave the regions empty. This is
  /// used to abstract away the optional underlying region creation.
  /// This does not change the balance between input, output_buffer
  /// and init_tensors operands.
  Operation *cloneWithoutRegions(OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands);
};
namespace detail {
  template <typename ConcreteOp>
  struct DestinationStyleOpInterfaceTrait : public ::mlir::OpInterface<DestinationStyleOpInterface, detail::DestinationStyleOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    /// Return the number of outputs.
    int64_t getNumOutputs() {
      auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        return end - start;
    }
    /// Return the output operands.
    OpOperandVector getOutputOperands() {
      auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();

        OpOperandVector result;
        result.reserve(end - start);
        for (int i = start; i < end; ++i)
          result.push_back(&(*static_cast<ConcreteOp *>(this))->getOpOperand(i));
        return result;
    }
    /// Return the `i`-th output operand.
    OpOperand *getOutputOperand(int64_t i) {
      assert(i >= 0 && i < (*static_cast<ConcreteOp *>(this)).getNumOutputs());
        auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        return &(*static_cast<ConcreteOp *>(this))->getOpOperand(start + i);
    }
    /// Set the `i`-th output operand.
    void setOutputOperand(int64_t i, Value value) {
      assert(i >= 0 && i < (*static_cast<ConcreteOp *>(this)).getNumOutputs());
        auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        (*static_cast<ConcreteOp *>(this))->setOperand(start + i, value);
    }
    /// Return the number of inputs.
    int64_t getNumInputs() {
      return (*static_cast<ConcreteOp *>(this)).getNumOperands() - (*static_cast<ConcreteOp *>(this)).getNumOutputs();
    }
    /// Return the input operands.
    OpOperandVector getInputOperands() {
      auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        int64_t numOutputs = end - start;
        int64_t numOperands = (*static_cast<ConcreteOp *>(this)).getNumOperands();

        OpOperandVector result;
        result.reserve(numOperands - numOutputs);
        for (int i = 0; i < start; ++i)
          result.push_back(&(*static_cast<ConcreteOp *>(this))->getOpOperand(i));
        for (int i = end; i < numOperands; ++i)
          result.push_back(&(*static_cast<ConcreteOp *>(this))->getOpOperand(end + i));

        return result;
    }
    /// Return the `i`-th input operand.
    OpOperand *getInputOperand(int64_t i) {
      assert(i >= 0 && i < getNumInputs());
        auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        return &(*static_cast<ConcreteOp *>(this))->getOpOperand(i < start ? i : i + end - start) ;
    }
    /// Return true if `opOperand` is an input.
    bool isInput(OpOperand * opOperand) {
      auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        auto operandNumber = opOperand->getOperandNumber();
        return operandNumber < start || operandNumber >= end;
    }
    /// Return true if `opOperand` is an output.
    bool isOutput(OpOperand * opOperand) {
      auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        auto operandNumber = opOperand->getOperandNumber();
        return operandNumber >= start && operandNumber < end;
    }
    /// Return true if the `opOperand` is a scalar value.
    bool isScalar(OpOperand * opOperand) {
      assert(opOperand->getOwner() == this->getOperation());
        return !opOperand->get().getType().template isa<ShapedType>();
    }
    /// Return the result tied to `opOperand`.
    OpResult getTiedOpResult(OpOperand * opOperand) {
      assert(opOperand->getOwner() == this->getOperation());

        auto [start, end] = (*static_cast<ConcreteOp *>(this)).getOutputsPositionRange();
        int64_t resultIndex = opOperand->getOperandNumber() - start;
        assert(resultIndex >= 0 &&
               resultIndex < (*static_cast<ConcreteOp *>(this))->getNumResults() );
        return (*static_cast<ConcreteOp *>(this))->getResult(resultIndex);
    }
    /// Return whether the op has only MemRef input and outputs.
    bool hasBufferSemantics() {
      return (*static_cast<ConcreteOp *>(this))->getNumResults() == 0 &&
          llvm::all_of((*static_cast<ConcreteOp *>(this))->getOpOperands(),
            [&](OpOperand &opOperand) {
              return isScalar(&opOperand) ||
                     opOperand.get().getType().template isa<MemRefType>();
            });
    }
    /// Return whether the op has only RankedTensor input and outputs.
    bool hasTensorSemantics() {
      return llvm::all_of((*static_cast<ConcreteOp *>(this))->getOpOperands(),
          [&](OpOperand &opOperand) {
            return isScalar(&opOperand) ||
                   opOperand.get().getType().template isa<RankedTensorType>();
          });
    }
    static ::mlir::LogicalResult verifyRegionTrait(::mlir::Operation *op) {
      return detail::verifyDestinationStyleOpInterface(op);
    }
  };
}// namespace detail
template<typename ConcreteOp>
std::pair<int64_t, int64_t> detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getOutputsPositionRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
}
template<typename ConcreteOp>
int64_t detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getNumOutputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumOutputs();
}
template<typename ConcreteOp>
OpOperandVector detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getOutputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputOperands();
}
template<typename ConcreteOp>
OpOperand *detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputOperand(i);
}
template<typename ConcreteOp>
void detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::setOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i, Value value) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setOutputOperand(i, value);
}
template<typename ConcreteOp>
int64_t detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getNumInputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumInputs();
}
template<typename ConcreteOp>
OpOperandVector detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getInputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getInputOperands();
}
template<typename ConcreteOp>
OpOperand *detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getInputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getInputOperand(i);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::isInput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).isInput(opOperand);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::isOutput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).isOutput(opOperand);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::isScalar(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).isScalar(opOperand);
}
template<typename ConcreteOp>
OpResult detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::getTiedOpResult(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getTiedOpResult(opOperand);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::hasBufferSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).hasBufferSemantics();
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::hasTensorSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).hasTensorSemantics();
}
template<typename ConcreteOp>
Operation *detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::clone(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands) {
  BlockAndValueMapping bvm;
        OperationState state(
          loc, ConcreteOp::getOperationName(), operands, resultTypes,
          (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getAttrs());
        for (Region &r : (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getRegions())
          r.cloneInto(state.addRegion(), bvm);
        return b.create(state);
}
template<typename ConcreteOp>
Operation *detail::DestinationStyleOpInterfaceInterfaceTraits::Model<ConcreteOp>::cloneWithoutRegions(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands) {
  OperationState state(
          loc, ConcreteOp::getOperationName(), operands, resultTypes,
          (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getAttrs());
        for (size_t cnt = 0, e = (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getNumRegions(); cnt < e; ++cnt)
          state.addRegion();
        return b.create(state);
}
template<typename ConcreteOp>
std::pair<int64_t, int64_t> detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getOutputsPositionRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getOutputsPositionRange(tablegen_opaque_val);
}
template<typename ConcreteOp>
int64_t detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getNumOutputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getNumOutputs(tablegen_opaque_val);
}
template<typename ConcreteOp>
OpOperandVector detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getOutputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getOutputOperands(tablegen_opaque_val);
}
template<typename ConcreteOp>
OpOperand *detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i) {
  return static_cast<const ConcreteOp *>(impl)->getOutputOperand(tablegen_opaque_val, i);
}
template<typename ConcreteOp>
void detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setOutputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i, Value value) {
  return static_cast<const ConcreteOp *>(impl)->setOutputOperand(tablegen_opaque_val, i, value);
}
template<typename ConcreteOp>
int64_t detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getNumInputs(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getNumInputs(tablegen_opaque_val);
}
template<typename ConcreteOp>
OpOperandVector detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getInputOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getInputOperands(tablegen_opaque_val);
}
template<typename ConcreteOp>
OpOperand *detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getInputOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int64_t i) {
  return static_cast<const ConcreteOp *>(impl)->getInputOperand(tablegen_opaque_val, i);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::isInput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return static_cast<const ConcreteOp *>(impl)->isInput(tablegen_opaque_val, opOperand);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::isOutput(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return static_cast<const ConcreteOp *>(impl)->isOutput(tablegen_opaque_val, opOperand);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::isScalar(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return static_cast<const ConcreteOp *>(impl)->isScalar(tablegen_opaque_val, opOperand);
}
template<typename ConcreteOp>
OpResult detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getTiedOpResult(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpOperand * opOperand) {
  return static_cast<const ConcreteOp *>(impl)->getTiedOpResult(tablegen_opaque_val, opOperand);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::hasBufferSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->hasBufferSemantics(tablegen_opaque_val);
}
template<typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::hasTensorSemantics(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->hasTensorSemantics(tablegen_opaque_val);
}
template<typename ConcreteOp>
Operation *detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::clone(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands) {
  return static_cast<const ConcreteOp *>(impl)->clone(tablegen_opaque_val, b, loc, resultTypes, operands);
}
template<typename ConcreteOp>
Operation *detail::DestinationStyleOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::cloneWithoutRegions(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands) {
  return static_cast<const ConcreteOp *>(impl)->cloneWithoutRegions(tablegen_opaque_val, b, loc, resultTypes, operands);
}
template<typename ConcreteModel, typename ConcreteOp>
int64_t detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getNumOutputs(::mlir::Operation *tablegen_opaque_val) const {
auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        return end - start;
}
template<typename ConcreteModel, typename ConcreteOp>
OpOperandVector detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getOutputOperands(::mlir::Operation *tablegen_opaque_val) const {
auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();

        OpOperandVector result;
        result.reserve(end - start);
        for (int i = start; i < end; ++i)
          result.push_back(&(llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperand(i));
        return result;
}
template<typename ConcreteModel, typename ConcreteOp>
OpOperand *detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getOutputOperand(::mlir::Operation *tablegen_opaque_val, int64_t i) const {
assert(i >= 0 && i < (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumOutputs());
        auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        return &(llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperand(start + i);
}
template<typename ConcreteModel, typename ConcreteOp>
void detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::setOutputOperand(::mlir::Operation *tablegen_opaque_val, int64_t i, Value value) const {
assert(i >= 0 && i < (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumOutputs());
        auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        (llvm::cast<ConcreteOp>(tablegen_opaque_val))->setOperand(start + i, value);
}
template<typename ConcreteModel, typename ConcreteOp>
int64_t detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getNumInputs(::mlir::Operation *tablegen_opaque_val) const {
return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumOperands() - (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumOutputs();
}
template<typename ConcreteModel, typename ConcreteOp>
OpOperandVector detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getInputOperands(::mlir::Operation *tablegen_opaque_val) const {
auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        int64_t numOutputs = end - start;
        int64_t numOperands = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getNumOperands();

        OpOperandVector result;
        result.reserve(numOperands - numOutputs);
        for (int i = 0; i < start; ++i)
          result.push_back(&(llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperand(i));
        for (int i = end; i < numOperands; ++i)
          result.push_back(&(llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperand(end + i));

        return result;
}
template<typename ConcreteModel, typename ConcreteOp>
OpOperand *detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getInputOperand(::mlir::Operation *tablegen_opaque_val, int64_t i) const {
assert(i >= 0 && i < getNumInputs());
        auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        return &(llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperand(i < start ? i : i + end - start) ;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::isInput(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const {
auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        auto operandNumber = opOperand->getOperandNumber();
        return operandNumber < start || operandNumber >= end;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::isOutput(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const {
auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        auto operandNumber = opOperand->getOperandNumber();
        return operandNumber >= start && operandNumber < end;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::isScalar(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const {
assert(opOperand->getOwner() == this->getOperation());
        return !opOperand->get().getType().template isa<ShapedType>();
}
template<typename ConcreteModel, typename ConcreteOp>
OpResult detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getTiedOpResult(::mlir::Operation *tablegen_opaque_val, OpOperand *opOperand) const {
assert(opOperand->getOwner() == this->getOperation());

        auto [start, end] = (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getOutputsPositionRange();
        int64_t resultIndex = opOperand->getOperandNumber() - start;
        assert(resultIndex >= 0 &&
               resultIndex < (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getNumResults() );
        return (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getResult(resultIndex);
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::hasBufferSemantics(::mlir::Operation *tablegen_opaque_val) const {
return (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getNumResults() == 0 &&
          llvm::all_of((llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperands(),
            [&](OpOperand &opOperand) {
              return isScalar(&opOperand) ||
                     opOperand.get().getType().template isa<MemRefType>();
            });
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DestinationStyleOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::hasTensorSemantics(::mlir::Operation *tablegen_opaque_val) const {
return llvm::all_of((llvm::cast<ConcreteOp>(tablegen_opaque_val))->getOpOperands(),
          [&](OpOperand &opOperand) {
            return isScalar(&opOperand) ||
                   opOperand.get().getType().template isa<RankedTensorType>();
          });
}
} // namespace mlir
