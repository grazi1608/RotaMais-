from models import db
from models.motorista import Motorista
from models.corrida import Corrida


class RelatorioRepository:
    """Consultas especiais de relatório (agregações/agrupamentos) que não
    fazem sentido morar na Model nem no Service — apenas acesso a dados
    complexo, sem regra de negócio."""

    def lucro_por_motorista(self):
        """Agrupa as corridas por motorista e soma valor, custo e lucro."""
        resultados = (
            db.session.query(
                Motorista.id,
                Motorista.nome,
                db.func.count(Corrida.id).label("total_corridas"),
                db.func.coalesce(db.func.sum(Corrida.valor), 0).label("total_faturado"),
                db.func.coalesce(db.func.sum(Corrida.custo_estimado), 0).label("total_custo"),
                db.func.coalesce(db.func.sum(Corrida.lucro), 0).label("total_lucro"),
            )
            .outerjoin(Corrida, Corrida.motorista_id == Motorista.id)
            .group_by(Motorista.id, Motorista.nome)
            .order_by(db.func.coalesce(db.func.sum(Corrida.lucro), 0).desc())
            .all()
        )

        return [
            {
                "motorista_id": linha.id,
                "motorista_nome": linha.nome,
                "total_corridas": linha.total_corridas,
                "total_faturado": float(linha.total_faturado),
                "total_custo": float(linha.total_custo),
                "total_lucro": float(linha.total_lucro),
            }
            for linha in resultados
        ]
