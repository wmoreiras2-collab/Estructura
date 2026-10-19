"""Prueba automatica del sistema de ventas + devoluciones (usa los controladores, no el menu)."""
import os
import shutil
import tempfile
from datetime import date, timedelta

from views import (ClienteController, ProductoController, VentaController,
                   DevolucionController)

carpeta = tempfile.mkdtemp()
try:
    ruta = lambda nombre: os.path.join(carpeta, nombre)
    cli = ClienteController(ruta("clientes.json"))
    pro = ProductoController(ruta("productos.json"))
    ven = VentaController(cli, pro, ruta("ventas.json"))
    dev = DevolucionController(ven, pro, ruta("devoluciones.json"))

    def ok(titulo, resultado, esperado):
        marca = "OK   " if resultado[0] == esperado else "FALLA"
        print(f"[{marca}] {titulo}: {resultado[1]}")
        assert resultado[0] == esperado, titulo

    # ---------- Ventas (lo que ya existia) ----------
    ok("crear cliente", cli.crear({"nombre": "ana", "apellido": "perez", "email": "ana@x.com",
                                   "telefono": "0987654321", "ciudad": "guayaquil"}), True)
    ok("crear teclado", pro.crear({"nombre": "teclado", "precio": "25.5", "stock": "6"}), True)
    ok("crear mouse", pro.crear({"nombre": "mouse", "precio": "12", "stock": "3"}), True)
    ok("venta de 2 teclados", ven.crear({"cliente_id": 1, "producto_id": 1, "cantidad": 2}), True)
    ok("anular venta sin devoluciones", dev.anular_venta(1), True)
    assert pro.obtener(1).stock == 6

    # ---------- Devoluciones: la secuencia 16.6 de la guia ----------
    ok("venta de 3 mouse", ven.crear({"cliente_id": 1, "producto_id": 2, "cantidad": 3}), True)
    assert pro.obtener(2).stock == 0
    V = ven.leer()[-1].id            # id de la venta de 3 mouse (el id 1 se reutilizo al anular)
    ok("venta inexistente", dev.crear({"venta_id": 99, "cantidad": 1, "motivo": "arrepentido"}), False)
    ok("devolver 5 de 3", dev.crear({"venta_id": V, "cantidad": 5, "motivo": "arrepentido"}), False)
    ok("cantidad 0", dev.crear({"venta_id": V, "cantidad": 0, "motivo": "arrepentido"}), False)
    ok("cantidad texto", dev.crear({"venta_id": V, "cantidad": "x", "motivo": "arrepentido"}), False)
    ok("motivo roto", dev.crear({"venta_id": V, "cantidad": 2, "motivo": "roto"}), False)
    assert len(dev.leer()) == 0, "no debe registrarse nada con errores"
    ok("devolver 2 arrepentido", dev.crear({"venta_id": V, "cantidad": 2, "motivo": "arrepentido"}), True)
    assert dev.obtener(1).monto == 27.6 and pro.obtener(2).stock == 2
    ok("devolver 1 defectuoso", dev.crear({"venta_id": V, "cantidad": 1, "motivo": "defectuoso"}), True)
    assert dev.obtener(2).monto == 13.8 and pro.obtener(2).stock == 2, "defectuoso no regresa al stock"
    ok("ya no hay disponibles", dev.crear({"venta_id": V, "cantidad": 1, "motivo": "arrepentido"}), False)
    venta = ven.obtener(V)
    assert dev.cantidad_devuelta(V) == 3 and dev.cantidad_disponible(venta) == 0
    assert [d.id for d in dev.devoluciones_de_venta(V)] == [1, 2]
    assert dev.total_reembolsado() == 41.4 and dev.reembolsado_de_venta(V) == 41.4
    assert {k: len(v) for k, v in dev.devoluciones_por_motivo().items()} == {"arrepentido": 1, "defectuoso": 1}
    assert len(dev.buscar("defectuoso")) == 1 and len(dev.buscar(date.today().strftime("%Y-%m"))) == 2
    print(dev.nota_credito(1))
    print(dev.nota_credito(2))
    ok("actualizar devolucion", dev.actualizar(1, {}), False)
    ok("eliminar devolucion", dev.eliminar(1), False)
    ok("anular venta con devoluciones", dev.anular_venta(V), False)
    assert ven.obtener(V) is not None and ven.obtener(V).cantidad == 3, "la venta no se toca"

    # ---------- Plazo de 30 dias ----------
    ok("venta nueva de 1 mouse", pro.actualizar(2, {"stock": "5"}), True)
    ok("venta nueva", ven.crear({"cliente_id": 1, "producto_id": 2, "cantidad": 1}), True)
    W = ven.leer()[-1].id
    ven.obtener(W).fecha = (date.today() - timedelta(days=40)).isoformat()
    ven.guardar()
    ok("fuera del plazo (40 dias)", dev.crear({"venta_id": W, "cantidad": 1, "motivo": "arrepentido"}), False)
    ven.obtener(W).fecha = (date.today() - timedelta(days=30)).isoformat()
    ok("justo en el limite (30 dias)", dev.crear({"venta_id": W, "cantidad": 1, "motivo": "equivocado"}), True)

    # ---------- Persistencia ----------
    cli2 = ClienteController(ruta("clientes.json"))
    pro2 = ProductoController(ruta("productos.json"))
    ven2 = VentaController(cli2, pro2, ruta("ventas.json"))
    dev2 = DevolucionController(ven2, pro2, ruta("devoluciones.json"))
    assert len(dev2.leer()) == 3 and dev2.total_reembolsado() == round(41.4 + 13.8, 2)
    assert pro2.obtener(2).stock == 5 - 1 + 1, pro2.obtener(2).stock
    print("\nTODAS LAS PRUEBAS PASARON")
finally:
    shutil.rmtree(carpeta)
