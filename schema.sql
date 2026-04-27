CREATE TABLE IF NOT EXISTS nota_fiscal (
    id_nf       INTEGER PRIMARY KEY,
    chave_acesso TEXT NOT NULL,
    fornecedor  TEXT    NOT NULL,
    cnpj_fornecedor     INTEGER NOT NULL,
    descricao   TEXT    NOT NULL,
    nf_valor       REAL    NOT NULL,
    data_emissao        DATE    NOT NULL,
    data_vencimento DATE NOT NULL,
    categoria TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lancamentos_contabeis (
    id_lc       INTEGER PRIMARY KEY,
    id_nf INTEGER NOT NULL,
    fornecedor  TEXT    NOT NULL,
    cnpj_fornecedor INTEGER NOT NULL,
    descricao   TEXT    NOT NULL,
    lc_valor       REAL    NOT NULL,
    data_lancamento        DATE    NOT NULL,
    conta_debito TEXT NOT NULL,
    conta_credito TEXT NOT NULL
    FOREIGN KEY (id_nf) REFERENCES nota_fiscal(id_nf)
);

CREATE TABLE IF NOT EXISTS conciliacao (
    id_conciliacao      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_lc               INTEGER NOT NULL,
    id_nf               INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    valor_nota_fiscal   REAL    NOT NULL,
    valor_lancamento    REAL    NOT NULL,
    status              TEXT    NOT NULL,
    data_conciliacao    DATE    NOT NULL,
    FOREIGN KEY (id_lc) REFERENCES lancamentos_contabeis(id_lc),
    FOREIGN KEY (id_nf) REFERENCES nota_fiscal(id_nf)
);

CREATE TRIGGER trigger_conciliacao
AFTER INSERT ON lancamentos_contabeis
FOR EACH ROW
BEGIN

    INSERT INTO conciliacao (
        id_lc,
        id_nf,
        descricao,
        valor_nota_fiscal,
        valor_lancamento,
        status,
        data_conciliacao
    )
    SELECT
        NEW.id_lc,
        NEW.id_nf,

        -- DESCRIÇÃO
        CASE
            WHEN NEW.lc_valor < nf.nf_valor THEN
                'VALOR LANCADO MENOR QUE A NOTA'
            WHEN NEW.lc_valor > nf.nf_valor THEN
                'VALOR LANCADO MAIOR QUE A NOTA'
            ELSE
                'VALOR CORRETO'
        END,

        nf.nf_valor,
        NEW.lc_valor,

        -- STATUS
        CASE
            WHEN NEW.lc_valor = nf.nf_valor THEN
                'EM CONFORMIDADE'
            ELSE
                'DIVERGENCIA'
        END,

        datetime('now')

    FROM nota_fiscal nf
    WHERE nf.id_nf = NEW.id_nf;

END;

