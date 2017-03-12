import tvm
import numpy

def test_makeapi():
    """Not yet working, mock design"""
    n = tvm.Var('n')
    A = tvm.placeholder((n,), name='A')
    B = tvm.placeholder((n,), name='B')
    C = tvm.compute(A.shape, lambda *i: A(*i) + B(*i), name='C')
    s = tvm.Schedule(C.op)

    bounds = tvm.schedule.InferBound(s)
    stmt = tvm.schedule.ScheduleOps(s, bounds)

    Ab = tvm.Buffer(A.shape, A.dtype, name='A')
    Bb = tvm.Buffer(B.shape, B.dtype, name='B')
    Cb = tvm.Buffer(C.shape, C.dtype, name='C')
    stmt = tvm.ir_pass.StorageFlatten(stmt, {A: Ab, B:Bb, C:Cb})

    num_unpacked_args = 2
    f = tvm.ir_pass.MakeAPI(
        stmt, "myadd", [n, Ab, Bb, Cb], num_unpacked_args)
    assert(f.handle_data_type[Ab.data].dtype == Ab.dtype)
    assert(len(f.args) == 5)
    output_ssa = False


if __name__ == "__main__":
    test_makeapi()