WITH ganho_total AS (
	SELECT
		cl.nome,
		isnull(tr.percentual_desconto, 0) AS percentual_desconto,
		(tr.valor_total * cn.percentual) AS valor_total_cl
	FROM
		transacao tr
	JOIN
		contrato cn ON tr.contrato_id = cn.contrato_id
	JOIN
		cliente cl ON cn.cliente_id = cl.cliente_id
	WHERE cn.ativo <> 0
)
SELECT
	gt.nome AS cliente_nome,
	sum((gt.valor_total_cl - (gt.valor_total_cl * (gt.percentual_desconto / 100 ))) / 100) AS valor
FROM
	ganho_total gt
GROUP BY
	gt.nome;
