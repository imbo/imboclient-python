<?php
namespace Imbo;

return array(
    'accessControl' => function() {
        return new Auth\AccessControl\Adapter\SimpleArrayAdapter([
            'test' => 'test',
        ]);
    },

    'database' => function() {
        return new Database\MongoDB(array(
            'databaseName' => 'imbo-develop',
        ));
    },

    'storage' => function() {
        return new Storage\GridFS(array(
            'databaseName' => 'imbo-develop-storage',
        ));
    }
);
