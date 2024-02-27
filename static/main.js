
    function atualizarEstado(tarefaId, concluida) {
        fetch(`/editar/${tarefaId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ concluida: concluida }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao atualizar estado da tarefa');
            }
            // Se necessário, você pode adicionar alguma lógica aqui para atualizar a interface do usuário.
        })
        .catch(error => {
            console.error('Erro:', error);
            // Se necessário, você pode adicionar alguma lógica aqui para lidar com o erro.
        });
    }

