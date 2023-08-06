/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/// Return start and end indices of the output operands range.
std::pair<int64_t, int64_t> mlir::DestinationStyleOpInterface::getOutputsPositionRange() {
      return getImpl()->getOutputsPositionRange(getImpl(), getOperation());
  }
/// Return the number of outputs.
int64_t mlir::DestinationStyleOpInterface::getNumOutputs() {
      return getImpl()->getNumOutputs(getImpl(), getOperation());
  }
/// Return the output operands.
OpOperandVector mlir::DestinationStyleOpInterface::getOutputOperands() {
      return getImpl()->getOutputOperands(getImpl(), getOperation());
  }
/// Return the `i`-th output operand.
OpOperand *mlir::DestinationStyleOpInterface::getOutputOperand(int64_t i) {
      return getImpl()->getOutputOperand(getImpl(), getOperation(), i);
  }
/// Set the `i`-th output operand.
void mlir::DestinationStyleOpInterface::setOutputOperand(int64_t i, Value value) {
      return getImpl()->setOutputOperand(getImpl(), getOperation(), i, value);
  }
/// Return the number of inputs.
int64_t mlir::DestinationStyleOpInterface::getNumInputs() {
      return getImpl()->getNumInputs(getImpl(), getOperation());
  }
/// Return the input operands.
OpOperandVector mlir::DestinationStyleOpInterface::getInputOperands() {
      return getImpl()->getInputOperands(getImpl(), getOperation());
  }
/// Return the `i`-th input operand.
OpOperand *mlir::DestinationStyleOpInterface::getInputOperand(int64_t i) {
      return getImpl()->getInputOperand(getImpl(), getOperation(), i);
  }
/// Return true if `opOperand` is an input.
bool mlir::DestinationStyleOpInterface::isInput(OpOperand * opOperand) {
      return getImpl()->isInput(getImpl(), getOperation(), opOperand);
  }
/// Return true if `opOperand` is an output.
bool mlir::DestinationStyleOpInterface::isOutput(OpOperand * opOperand) {
      return getImpl()->isOutput(getImpl(), getOperation(), opOperand);
  }
/// Return true if the `opOperand` is a scalar value.
bool mlir::DestinationStyleOpInterface::isScalar(OpOperand * opOperand) {
      return getImpl()->isScalar(getImpl(), getOperation(), opOperand);
  }
/// Return the result tied to `opOperand`.
OpResult mlir::DestinationStyleOpInterface::getTiedOpResult(OpOperand * opOperand) {
      return getImpl()->getTiedOpResult(getImpl(), getOperation(), opOperand);
  }
/// Return whether the op has only MemRef input and outputs.
bool mlir::DestinationStyleOpInterface::hasBufferSemantics() {
      return getImpl()->hasBufferSemantics(getImpl(), getOperation());
  }
/// Return whether the op has only RankedTensor input and outputs.
bool mlir::DestinationStyleOpInterface::hasTensorSemantics() {
      return getImpl()->hasTensorSemantics(getImpl(), getOperation());
  }
/// Clone the current operation with the given location and operands. This
/// is used to abstract away the optional underlying region creation. This
/// does not change the balance between input, output_buffer and
/// init_tensors operands.
Operation *mlir::DestinationStyleOpInterface::clone(OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands) {
      return getImpl()->clone(getImpl(), getOperation(), b, loc, resultTypes, operands);
  }
/// Clone the current operation with the given location, operands
/// and BlockAndValueMapping but leave the regions empty. This is
/// used to abstract away the optional underlying region creation.
/// This does not change the balance between input, output_buffer
/// and init_tensors operands.
Operation *mlir::DestinationStyleOpInterface::cloneWithoutRegions(OpBuilder & b, Location loc, TypeRange resultTypes, ValueRange operands) {
      return getImpl()->cloneWithoutRegions(getImpl(), getOperation(), b, loc, resultTypes, operands);
  }
