CREATE OR REPLACE PROCEDURE SPINCARE_CONTA_PACIENTE(p_id_conta              in CONTA_PACIENTE.Nr_Interno_Conta%TYPE,
                                                    p_nr_prescricao         IN PRESCR_MEDICA.nr_prescricao%TYPE,
                                                    p_ie_status_conta       IN CONTA_PACIENTE.IE_STATUS_ACERTO%TYPE,
                                                    p_cd_convenio_parametro IN CONTA_PACIENTE.CD_CONVENIO_PARAMETRO%TYPE,
                                                    p_cd_estabelecimento    IN CONTA_PACIENTE.CD_ESTABELECIMENTO%TYPE,
                                                    p_vl_conta              IN CONTA_PACIENTE.VL_CONTA%TYPE,
                                                    p_vl_desconto           IN CONTA_PACIENTE.VL_DESCONTO%TYPE,
                                                    p_nm_usuario            IN CONTA_PACIENTE.NM_USUARIO%TYPE DEFAULT 'spincare',
                                                    p_cd_servico            IN VARCHAR2,
                                                    p_qt_executado          IN VARCHAR2) IS
  v_nr_interno_conta      CONTA_PACIENTE.NR_INTERNO_CONTA%TYPE;
  v_dt_mesano_referencia  CONTA_PACIENTE.DT_MESANO_REFERENCIA%TYPE;
  v_nr_atendimento        PRESCR_MEDICA.nr_atendimento%TYPE;
  v_nr_prescricao         PRESCR_MEDICA.NR_PRESCRICAO%TYPE;
  v_cd_convenio_parametro CONTA_PACIENTE.Cd_Convenio_Parametro%TYPE;
  v_nr_sequencia          NUMBER(10);
  v_dt_entrada_unidade    DATE; -- Data de entrada na unidade
  --  v_dt_procedimento      DATE; -- Data do procedimento
  v_cd_setor_atendimento NUMBER(5);
  v_nr_seq_atepacu       NUMBER(10);
  detail_w               VARCHAR2(4000);
  v_idx                  PLS_INTEGER := 1;
  v_total                PLS_INTEGER := REGEXP_COUNT(p_cd_servico, '\|') + 1;
  v_spincare_id          VARCHAR2(50);
  v_tasy_id              NUMBER;
  v_qtd                  NUMBER; -- Cursor para buscar os procedimentos relacionados ? prescri??o
  v_conta_ja_integrada   NUMBER := 0;
BEGIN

  -- Verifica se a conta já foi integrada
  SELECT max(codigo_tasy)
    INTO v_conta_ja_integrada
    FROM mapa_codigo_integracao
   WHERE codigo_spincare = p_id_conta
     AND nome_integracao = 'Conta';

  IF v_conta_ja_integrada > 0 THEN
    -- Conta já integrada — comportamento a ser definido:
    DELETE FROM PROCEDIMENTO_PACIENTE
     WHERE NR_INTERNO_CONTA = v_nr_interno_conta;
  else 
    begin
    
      -- Obter o pr?ximo valor da sequ?ncia para NR_INTERNO_CONTA
    SELECT conta_paciente_seq.NEXTVAL INTO v_nr_interno_conta FROM dual;

    -- Obter o DT_MESANO_REFERENCIA mais recente
    SELECT DT_MESANO_VIGENTE
      INTO v_dt_mesano_referencia
      FROM PARAMETRO_ESTOQUE
     ORDER BY DT_MESANO_VIGENTE DESC FETCH FIRST ROW ONLY;

    -- Formatar detalhes para o log no formato JSON
    detail_w := '{"p_nr_prescricao": "' || p_nr_prescricao || '", ' ||
                '"ie_status_acerto": "' || p_ie_status_conta || '", ' ||
                '"dt_acerto_conta": "' ||
                TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') || '", ' ||
                '"dt_periodo_inicial": "' ||
                TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') || '", ' ||
                '"dt_periodo_final": "' ||
                TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') || '", ' ||
                '"dt_atualizacao": "' ||
                TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') || '", ' ||
                '"nm_usuario": "' || p_nm_usuario || '", ' ||
                '"p_cd_convenio_parametro": "' || p_cd_convenio_parametro ||
                '", ' || '"nr_interno_conta": "' || v_nr_interno_conta ||
                '", ' || '"cd_estabelecimento": "' || p_cd_estabelecimento ||
                '", ' || '"vl_conta": "' || p_vl_conta || '", ' ||
                '"vl_desconto": "' || NVL(p_vl_desconto, 0) || '", ' ||
                '"dt_mesano_referencia": "' ||
                TO_CHAR(v_dt_mesano_referencia, 'YYYY-MM-DD') || '", ' ||
                '"cds_servicos: "' || p_cd_servico || '", ' ||
                '"p_qt_executado: "' || p_qt_executado || '", ' ||
                '"status": "Insert iniciado"}';

    BEGIN
      SELECT p.nr_atendimento, a.dt_entrada, p.nr_prescricao
        INTO v_nr_atendimento, v_dt_entrada_unidade, v_nr_prescricao
        FROM PRESCR_MEDICA p
        JOIN mapa_codigo_integracao m
          ON p.nr_prescricao = m.codigo_tasy
        JOIN atendimento_paciente a
          ON a.nr_atendimento = p.nr_atendimento
       WHERE m.nome_integracao = 'prescricao'
         AND m.codigo_spincare = p_nr_prescricao;
    EXCEPTION
      WHEN NO_DATA_FOUND THEN
        detail_w := detail_w ||
                    ', "erro": "N?o encontrado v?nculo para prescri??o (p_nr_prescricao: ' ||
                    p_nr_prescricao || ')"';
        insert_log_integracao_spincare(p_log_level   => 'ERROR',
                                       p_message     => 'Erro buscando prescri??o e atendimento.',
                                       p_source      => 'SPINCARE_CONTA_PACIENTE',
                                       p_details     => detail_w,
                                       p_error_stack => 'Prescri??o/Atendimento n?o encontrado');
        RAISE_APPLICATION_ERROR(-20001,
                                'Erro: Prescri??o/Atendimento n?o encontrado para codigo_spincare = ' ||
                                p_nr_prescricao ||
                                ' na mapa_codigo_integracao onde nome_integracao = prescricao');
    END;

    detail_w := REPLACE(detail_w,
                        '"p_nr_prescricao": "' || p_nr_prescricao || '", ',
                        '"p_nr_prescricao": "' || p_nr_prescricao ||
                        '", "v_nr_atendimento": "' || v_nr_atendimento ||
                        '", ');

    BEGIN
      SELECT codigo_tasy
        INTO v_cd_convenio_parametro
        FROM mapa_codigo_integracao
       WHERE codigo_spincare = p_cd_convenio_parametro
         AND nome_integracao = 'Convenio';
    EXCEPTION
      WHEN NO_DATA_FOUND THEN
        detail_w := detail_w ||
                    ', "erro": "N?o encontrado v?nculo de conv?nio (p_cd_convenio_parametro: ' ||
                    p_cd_convenio_parametro || ')"';
        insert_log_integracao_spincare(p_log_level   => 'ERROR',
                                       p_message     => 'Erro buscando c?digo_tasy do conv?nio.',
                                       p_source      => 'SPINCARE_CONTA_PACIENTE',
                                       p_details     => detail_w,
                                       p_error_stack => 'Conv?nio n?o encontrado');
        RAISE_APPLICATION_ERROR(-20001,
                                'Erro: Conv?nio n?o encontrado para c?digo_spincare = ' ||
                                p_cd_convenio_parametro ||
                                ' na mapa_codigo_integracao onde nome_integracao = Convenio');
    END;

    detail_w := REPLACE(detail_w,
                        '"p_cd_convenio_parametro": "' ||
                        p_cd_convenio_parametro || '", ',
                        '"p_cd_convenio_parametro": "' ||
                        p_cd_convenio_parametro ||
                        '", "v_cd_convenio_parametro": "' ||
                        v_cd_convenio_parametro || '", ');

    BEGIN
      SELECT a.nr_seq_interno, a.cd_setor_atendimento
        INTO v_nr_seq_atepacu, v_cd_setor_atendimento
        FROM ATEND_PACIENTE_UNIDADE a
        JOIN PRESCR_MEDICA p
          ON a.nr_atendimento = p.nr_atendimento
        JOIN mapa_codigo_integracao m
          ON p.nr_prescricao = m.codigo_tasy
       WHERE m.nome_integracao = 'prescricao'
         AND m.codigo_spincare = p_nr_prescricao;
    EXCEPTION
      WHEN NO_DATA_FOUND THEN
        detail_w := detail_w ||
                    ', "erro": "N?o encontrado v?nculo com ATEND_PACIENTE_UNIDADE (p_nr_prescricao: ' ||
                    p_nr_prescricao || ')"';
        insert_log_integracao_spincare(p_log_level   => 'ERROR',
                                       p_message     => 'Erro buscando ATEND_PACIENTE_UNIDADE.',
                                       p_source      => 'SPINCARE_CONTA_PACIENTE',
                                       p_details     => detail_w,
                                       p_error_stack => 'Sequ?ncia interna/setor n?o encontrado');
        RAISE_APPLICATION_ERROR(-20001,
                                'Erro: ATEND_PACIENTE_UNIDADE n?o encontrado para p_nr_prescricao = ' ||
                                p_nr_prescricao);
    END;

    -- Inserir os dados na tabela CONTA_PACIENTE
    INSERT INTO CONTA_PACIENTE
      (NR_ATENDIMENTO,
       IE_STATUS_ACERTO,
       DT_ACERTO_CONTA,
       DT_PERIODO_INICIAL,
       DT_PERIODO_FINAL,
       DT_ATUALIZACAO,
       NM_USUARIO,
       CD_CONVENIO_PARAMETRO,
       NR_INTERNO_CONTA,
       CD_ESTABELECIMENTO,
       VL_CONTA,
       VL_DESCONTO,
       DT_MESANO_REFERENCIA)
    VALUES
      (v_nr_atendimento, -- N?mero do atendimento
       p_ie_status_conta, -- Status da conta
       SYSDATE, -- Data de acerto da conta
       SYSDATE, -- Data do per?odo inicial
       SYSDATE, -- Data do per?odo final
       SYSDATE, -- Data de atualiza??o
       p_nm_usuario, -- Nome do usu?rio
       v_cd_convenio_parametro, -- C?digo do conv?nio
       v_nr_interno_conta, -- N?mero interno da conta
       p_cd_estabelecimento, -- C?digo do estabelecimento
       p_vl_conta, -- Valor da conta
       NVL(p_vl_desconto, 0), -- Valor do desconto (enviar zero se n?o tiver)
       v_dt_mesano_referencia -- Data do m?s/ano de refer?ncia
       );

    detail_w := REPLACE(detail_w,
                        '"p_cd_convenio_parametro": "' ||
                        p_cd_convenio_parametro || '", ',
                        '"p_cd_convenio_parametro": "' ||
                        p_cd_convenio_parametro ||
                        '", "v_cd_convenio_parametro": "' ||
                        v_cd_convenio_parametro || '", ');
  end if; 
  
WHILE v_idx <= v_total LOOP
-- Extrai os valores da posição atual do array
v_spincare_id := REGEXP_SUBSTR(p_cd_servico, '[^|]+', 1, v_idx); v_qtd := TO_NUMBER(REGEXP_SUBSTR(p_qt_executado, '[^|]+', 1, v_idx));

  -- Converte código_spincare para código_tasy
BEGIN
SELECT TO_NUMBER(codigo_tasy) INTO v_tasy_id FROM mapa_codigo_integracao WHERE codigo_spincare = v_spincare_id AND nome_integracao = 'Procedimento';
EXCEPTION
WHEN NO_DATA_FOUND THEN insert_log_integracao_spincare(p_log_level => 'ERROR', p_message => 'Procedimento não encontrado no mapa de integração.', p_source => 'SPINCARE_CONTA_PACIENTE', p_details => 'codigo_spincare: ' || v_spincare_id, p_error_stack => 'Sem vínculo no mapa_codigo_integracao');
-- Opcional: você pode continuar o loop ou abortar com RAISE_APPLICATION_ERROR
v_idx := v_idx + 1; CONTINUE;
END;

  -- Gera a sequência
v_nr_sequencia := procedimento_paciente_seq.NEXTVAL;

  -- Faz o insert com o código traduzido e a quantidade
INSERT INTO PROCEDIMENTO_PACIENTE(NR_SEQUENCIA, NR_ATENDIMENTO, DT_ENTRADA_UNIDADE, CD_PROCEDIMENTO, DT_PROCEDIMENTO, QT_PROCEDIMENTO, DT_ATUALIZACAO, NM_USUARIO, CD_SETOR_ATENDIMENTO, IE_ORIGEM_PROCED, NR_SEQ_ATEPACU, NR_INTERNO_CONTA) VALUES(v_nr_sequencia, v_nr_atendimento, v_dt_entrada_unidade, v_tasy_id, v_dt_entrada_unidade, v_qtd, SYSDATE, p_nm_usuario, v_cd_setor_atendimento, NULL, v_nr_seq_atepacu, v_nr_interno_conta);

  -- Atualiza o preço do procedimento
ATUALIZA_PRECO_PROCEDIMENTO(v_nr_sequencia, v_cd_convenio_parametro, 'pulsati.jonas');

  -- Avança para o próximo item do array
v_idx := v_idx + 1;

END LOOP;

  -- Inserir v?nculos no mapa_codigo_integracao
INSERT INTO mapa_codigo_integracao(codigo_spincare, codigo_tasy, nome_integracao) VALUES(p_id_conta, v_nr_interno_conta, 'Conta');

  -- Log de sucesso na integra??o
insert_log_integracao_spincare(p_log_level => 'INFO', p_message => 'Opera??o bem-sucedida na tabela CONTA_PACIENTE.', p_source => 'SPINCARE_CONTA_PACIENTE', p_details => detail_w);

  -- Commit para confirmar a opera??o
COMMIT;
EXCEPTION
WHEN OTHERS THEN
-- Em caso de erro, rollback e log
ROLLBACK; insert_log_integracao_spincare(p_log_level => 'ERROR', p_message => 'Erro na opera??o com a tabela CONTA_PACIENTE.', p_source => 'SPINCARE_CONTA_PACIENTE', p_details => detail_w, p_error_stack => SQLERRM);

  -- Commit
COMMIT; RAISE_APPLICATION_ERROR(-20001, 'Erro ao inserir na CONTA PACIENTE: ' || SQLERRM);
END SPINCARE_CONTA_PACIENTE;
