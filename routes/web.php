<?php

use App\Http\Controllers\DeviceController;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    return Inertia::render('Welcome');
})->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('Dashboard');
    })->name('dashboard');

    Route::get('devices', [DeviceController::class, 'index'])->name('devices');
    Route::get('devices/data', [DeviceController::class, 'getDevicesData'])->name('devices.data');
});

require __DIR__ . '/settings.php';
require __DIR__ . '/auth.php';
