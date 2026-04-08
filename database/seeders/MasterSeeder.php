<?php

namespace Database\Seeders;

use App\Models\Organization;
use App\Models\User;
use App\Models\Status;
use Illuminate\Support\Facades\Hash;
use Illuminate\Database\Seeder;
use Illuminate\Support\Str;

class MasterSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        Status::create(
            ['name' => 'Aktif']
        );

        Status::create(
            ['name' => 'Tidak Aktif']
        );

        $parent = Organization::create(['short_code' => '00', 'long_code' => '3500', 'name' => 'JAWA TIMUR', 'parent_id' => null, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '01', 'long_code' => '3501', 'name' => 'PACITAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '02', 'long_code' => '3502', 'name' => 'PONOROGO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '03', 'long_code' => '3503', 'name' => 'TRENGGALEK', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '04', 'long_code' => '3504', 'name' => 'TULUNGAGUNG', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '05', 'long_code' => '3505', 'name' => 'BLITAR', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '06', 'long_code' => '3506', 'name' => 'KEDIRI', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '07', 'long_code' => '3507', 'name' => 'MALANG', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '08', 'long_code' => '3508', 'name' => 'LUMAJANG', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '09', 'long_code' => '3509', 'name' => 'JEMBER', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '10', 'long_code' => '3510', 'name' => 'BANYUWANGI', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '11', 'long_code' => '3511', 'name' => 'BONDOWOSO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '12', 'long_code' => '3512', 'name' => 'SITUBONDO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '13', 'long_code' => '3513', 'name' => 'PROBOLINGGO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '14', 'long_code' => '3514', 'name' => 'PASURUAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '15', 'long_code' => '3515', 'name' => 'SIDOARJO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '16', 'long_code' => '3516', 'name' => 'MOJOKERTO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '17', 'long_code' => '3517', 'name' => 'JOMBANG', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '18', 'long_code' => '3518', 'name' => 'NGANJUK', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '19', 'long_code' => '3519', 'name' => 'MADIUN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '20', 'long_code' => '3520', 'name' => 'MAGETAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '21', 'long_code' => '3521', 'name' => 'NGAWI', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '22', 'long_code' => '3522', 'name' => 'BOJONEGORO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '23', 'long_code' => '3523', 'name' => 'TUBAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '24', 'long_code' => '3524', 'name' => 'LAMONGAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '25', 'long_code' => '3525', 'name' => 'GRESIK', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '26', 'long_code' => '3526', 'name' => 'BANGKALAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '27', 'long_code' => '3527', 'name' => 'SAMPANG', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '28', 'long_code' => '3528', 'name' => 'PAMEKASAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '29', 'long_code' => '3529', 'name' => 'SUMENEP', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '71', 'long_code' => '3571', 'name' => 'KEDIRI', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '72', 'long_code' => '3572', 'name' => 'BLITAR', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '73', 'long_code' => '3573', 'name' => 'MALANG', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '74', 'long_code' => '3574', 'name' => 'PROBOLINGGO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '75', 'long_code' => '3575', 'name' => 'PASURUAN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '76', 'long_code' => '3576', 'name' => 'MOJOKERTO', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '77', 'long_code' => '3577', 'name' => 'MADIUN', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '78', 'long_code' => '3578', 'name' => 'SURABAYA', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);
        Organization::create(['short_code' => '79', 'long_code' => '3579', 'name' => 'BATU', 'parent_id' => $parent->id, 'id' => Str::uuid(),]);


        User::create([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => Hash::make('123'),
        ]);
    }
}
