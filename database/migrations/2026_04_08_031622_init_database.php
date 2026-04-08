<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('organizations', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('short_code');
            $table->string('long_code');
            $table->string('name');
            $table->foreignUuid(column: 'parent_id')->nullable()->constrained('organizations');
        });

        Schema::table('users', function (Blueprint $table) {
            $table->foreignUuid(column: 'organization_id')->nullable()->constrained('organizations');
            $table->string('phone')->nullable();
        });

        Schema::create('statuses', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();
        });

        Schema::create('devices', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('id_bitdefender')->nullable();
            $table->string('nup')->nullable();
            $table->string('device_name')->nullable();
            $table->string('user')->nullable();
            $table->dateTime('last_update_at')->nullable();
            $table->foreignUuid(column: 'organization_id')->nullable()->constrained('organizations');
            $table->foreignId(column: 'status_id')->nullable()->constrained('statuses');
            $table->string('created_by')->nullable();
            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('devices');
        Schema::dropIfExists('statuses');
        Schema::dropIfExists('organizations');
    }
};
