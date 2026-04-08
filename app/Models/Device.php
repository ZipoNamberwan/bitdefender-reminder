<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Device extends Model
{
    use HasUuids;

    public function organization()
    {
        return $this->belongsTo(Organization::class, 'organization_id');
    }

    public function status()
    {
        return $this->belongsTo(Status::class, 'status_id');
    }
}
